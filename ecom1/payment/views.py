from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from account.models import Address
from home.models import Cart, Coupon
from home.views import get_cart_items
from .models import Order, OrderLine
from .forms import CheckoutForm
import stripe
from django.conf import settings
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Order
from django.urls import reverse



# Initialize Razorpay client
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
@transaction.atomic
def checkout_view(request):
    cart_items = get_cart_items(request)

    if not cart_items:
        messages.error(request, "Your cart is empty.")
        return redirect('home:cart')

    # Calculate total price before any discounts
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    # Handle coupons
    discount = Decimal('0.00')
    applied_coupon = None

    if 'coupon_id' in request.session:
        coupon_id = request.session['coupon_id']
        try:
            applied_coupon = Coupon.objects.get(id=coupon_id)
            discount = (applied_coupon.discount_percentage / 100) * total_price
        except Coupon.DoesNotExist:
            del request.session['coupon_id']
            messages.warning(request, "Invalid coupon code.")

    final_total = total_price - discount

    # Handle POST request
    if request.method == 'POST':
        selected_address_id = request.POST.get('selected_address')

        if not selected_address_id:
            messages.error(request, "Please select an address.")
            return redirect('payment:checkout')

        # Handle new address creation
        if selected_address_id == 'new':
            new_address = Address.objects.create(
                user=request.user,
                first_name=request.POST.get('new_first_name'),
                last_name=request.POST.get('new_last_name'),
                phone_number=request.POST.get('new_phone_number'),
                housename=request.POST.get('new_housename'),
                street=request.POST.get('new_street'),
                city=request.POST.get('new_city'),
                state=request.POST.get('new_state'),
                zipcode=request.POST.get('new_zipcode'),
            )
            shipping_address = new_address
        else:
            try:
                shipping_address = Address.objects.get(id=selected_address_id, user=request.user)
            except Address.DoesNotExist:
                messages.error(request, "Selected address not found.")
                return redirect('payment:checkout')

        # Create order
        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            total_price=final_total,
            is_paid=False,
        )

        # Add cart items to the order
        for item in cart_items:
            OrderLine.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                unit_price=item.product.price,
            )

        # Clear the cart
        Cart.objects.filter(user=request.user).delete()

        return redirect('payment:payment_method')

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'applied_coupon': applied_coupon,
        'discount': discount,
        'final_total': final_total,
        'addresses': Address.objects.filter(user=request.user),  # Fixed: Directly query Address
    }
    return render(request, 'payment/checkout.html', context)


# Ensure you set your Stripe Secret Key correctly
stripe.api_key = settings.STRIPE_SECRET_KEY

import logging
logger = logging.getLogger(__name__)

@login_required
def payment_method(request):
    # Fetch the unpaid order for the logged-in user
    order = Order.objects.filter(user=request.user, is_paid=False).first()
    if not order or not order.shipping_address:
        messages.error(request, "Please complete the checkout process first.")
        return redirect('payment:checkout')

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        if payment_method == 'cod':
            # Handle Cash on Delivery (COD)
            order.payment_method = 'COD'
            order.is_paid = True  # Mark as paid for COD
            order.save()
            # Directly move to order confirmation page after COD
            return redirect('payment:order_confirmation', order_id=order.id)

        elif payment_method == 'stripe':
            order.payment_method = 'Stripe'  # Set the payment method to Stripe
            try:
                # Create a Stripe PaymentIntent
                payment_intent = stripe.PaymentIntent.create(
                    amount=int(order.total_price * 100),  # Total in cents
                    currency="usd",
                    metadata={'order_id': order.id},  # Attach order ID to metadata
                )

                # Save the PaymentIntent ID for reference
                order.payment_id = payment_intent['id']
                order.save()

                # Pass the client secret to Stripe.js on the frontend
                return render(request, 'payment/stripe.html', {
                    'order': order,
                    'client_secret': payment_intent['client_secret'],
                    'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
                })
            except Exception as e:
                # Handle Stripe API errors
                messages.error(request, f"Stripe payment initiation failed: {str(e)}")
                return redirect('payment:payment_fail')

    return render(request, 'payment/payment_method.html', {'order': order})

@login_required
def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id)
    total_price = sum(item.get_total() for item in order.order_lines.all())
    applied_coupon = None  # If applicable
    discount = Decimal('0.00')  # If applicable
    final_total = total_price - discount  # After coupon, if any
    
    return render(request, 'payment/order_confirmation.html', {
        'order': order,
        'total_price': total_price,
        'applied_coupon': applied_coupon,
        'discount': discount,
        'final_total': final_total,
    })

@login_required
def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Mark the order as paid and update status
    order.is_paid = True
    order.save()

    messages.success(request, "Payment successful!")
    return redirect('payment:order_confirmation', order_id=order.id)

@login_required
def payment_fail(request):
    messages.error(request, "Payment failed. Please try again.")
    return render(request, 'payment/payment_fail.html')


@login_required
def order(request): 
    """
    Display a list of the user's orders, ordered by most recent.
    """
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'payment/order.html', {'orders': orders})


@login_required
def change_order_status(request, pid):
    """
    Change the status of an order. Only allow valid transitions based on the current status.
    """
    order = get_object_or_404(Order, id=pid)

    # Get the desired status from the query parameter
    status = request.GET.get('status')

    # Define allowed transitions (limited for current flow)
    allowed_transitions = {
        'Pending': ['Cancelled'],
        'Cancelled': [],
    }

    # Check if the transition is valid
    if status in allowed_transitions.get(order.status, []):
        order.status = status
        order.save()
        messages.success(request, f"Order status updated to '{status}'.")
    else:
        messages.error(request, f"Cannot change status from '{order.status}' to '{status}'.")

    # Redirect to the orders page
    return redirect(reverse('payment:order'))
