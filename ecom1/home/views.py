from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Category, Product, Cart, CartItem, Coupon, Wishlist,Carousel
from django.contrib.auth.decorators import login_required
from admin_panel.models import CustomUser  # Import CustomUser
from home.forms import CouponForm


def index(request):
    categories = Category.objects.all()  # Get all categories
    carousel_items = Carousel.objects.filter(active=True).order_by('order')  # Get active carousel items sorted by 'order'
    return render(request, 'home/index.html', {'categories': categories, 'carousel_items': carousel_items})

def product_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'home/product.html', {'products': products, 'category': category})

@login_required(login_url='account:login')
def product_detail(request, product_id):
    if not request.user.is_authenticated or request.user.is_superuser:
        messages.error(request, "You need to log in to access your cart.")
        return redirect('account:login')
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'home/product_detail.html', {'product': product})


@login_required(login_url='account:login')
def add_to_cart(request, product_id):
    if not request.user.is_authenticated or request.user.is_superuser:
        messages.error(request, "You need to log in to access your cart.")
        return redirect('account:login')

    product = get_object_or_404(Product, id=product_id)
    
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={"quantity": 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.info(request, "Increased product quantity in your cart.")
    else:
        messages.info(request, "Added product to your cart.")
    return redirect('home:cart')

@login_required(login_url='account:login')
def cart_view(request):
    # If the user is a superuser or an anonymous user, redirect to login
    if not request.user.is_authenticated or request.user.is_superuser:
        messages.error(request, "You need to log in to access your cart.")
        return redirect('account:login')

    # Fetch cart items for the logged-in user
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    # Handle coupon discount logic
    coupon_id = request.session.get('coupon_id')
    coupon = None
    discount = 0
    if coupon_id:
        try:
            coupon = Coupon.objects.get(id=coupon_id)
            discount = (coupon.discount_percentage / 100) * total_price
        except Coupon.DoesNotExist:
            messages.error(request, "Invalid coupon applied.")

    total_price_after_discount = total_price - discount

    # Create a coupon form for applying new coupons
    coupon_form = CouponForm()

    # Prepare context for the template
    context = {
        'cart_items': cart_items,
        'total_price': total_price,  # Original total price
        'coupon': coupon,            # Applied coupon details
        'discount': discount,        # Calculated discount
        'total_price_after_discount': total_price_after_discount,  # Final price after discount
        'coupon_form': coupon_form,  # Coupon form for user input
    }

    return render(request, 'home/cart.html', context)

@login_required
def get_cart_items(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user)
    return []

@login_required
def apply_coupon(request):
    if request.method == "POST":
        code = request.POST.get("coupon_code")
        try:
            coupon = Coupon.objects.get(code=code, active=True)
            request.session['coupon_id'] = coupon.id
            messages.success(request, f"Coupon '{code}' applied successfully!")
        except Coupon.DoesNotExist:
            messages.error(request, "Invalid or expired coupon code.")
            request.session['coupon_id'] = None
    return redirect('home:cart')

@login_required
def update_cart(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to update the cart.")
        return redirect('login')
    
    user = request.user
    for cart_item in Cart.objects.filter(user=user):
        quantity = request.POST.get(f'quantity_{cart_item.product.id}')
        if quantity and int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
            messages.success(request, f"Updated quantity for {cart_item.product.name}.")
        else:
            cart_item.delete()
            messages.info(request, f"Removed {cart_item.product.name} from your cart.")
    return redirect('home:cart')

@login_required
def remove_from_cart(request, product_id):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to remove items from the cart.")
        return redirect('login')
    
    product = get_object_or_404(Product, id=product_id)
    cart_item = Cart.objects.filter(user=request.user, product=product)
    if cart_item.exists():
        cart_item.delete()
        messages.success(request, f"Removed {product.name} from your cart.")
    else:
        messages.error(request, f"{product.name} was not found in your cart.")
    return redirect('home:cart')

@login_required
def update_cart_quantity(request, product_id, action):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if action == 'plus':
        cart_item.quantity += 1
    elif action == 'minus' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    cart_item.save()
    return redirect('home:cart')

@login_required(login_url='account:login')
def wishlist_view(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to remove items from the cart.")
        return redirect('login')
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'home/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('home:wishlist')

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    messages.success(request, "Item removed from your wishlist.")
    return redirect('home:wishlist')

@login_required
def move_to_cart(request, item_id):
    # Get the wishlist item using item_id
    wishlist_item = get_object_or_404(Wishlist, id=item_id, user=request.user)
    product = wishlist_item.product
    
    # Move the product to the cart if it's in the wishlist
    Cart.objects.create(user=request.user, product=product)
    wishlist_item.delete()  # Remove from wishlist
    messages.success(request, 'Product moved to cart.')
    
    return redirect('home:wishlist')

def search(request):
    query = request.GET.get('q', '').strip()  # Trim whitespace from the query
    products = Product.objects.filter(name__icontains=query) if query else []  # Case-insensitive search
    return render(request, 'home/search.html', {'products': products, 'query': query})

