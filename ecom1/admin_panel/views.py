from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.contrib import messages
from home.models import Product, Category
from home.forms import ProductForm
from home.models import Coupon,Carousel
from .forms import CouponForm,CarouselForm
from admin_panel.models import CustomUser
from account.forms import AddressForm
from payment.models import Order 

# Admin role check
def admin_required(user):
    return user.is_staff

# Admin Dashboard view
@login_required
@user_passes_test(admin_required)
def admin_dashboard(request):
    return render(request, 'admin_panel/admindashboard.html')

# User Management view
@login_required
@user_passes_test(admin_required)
def user_management(request):
    users = CustomUser.objects.all()  # Use CustomUser model
    return render(request, 'admin_panel/usermanagement.html', {'users': users})

# Activate user view
@login_required
@user_passes_test(admin_required)
def activate_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)  # Use CustomUser model
    user.is_active = True
    user.save()
    messages.success(request, 'User activated successfully.')
    return redirect('admin_panel:user_management')

# Deactivate user view
@login_required
@user_passes_test(admin_required)
def deactivate_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)  # Use CustomUser model
    user.is_active = False
    user.save()
    messages.success(request, 'User deactivated successfully.')
    return redirect('admin_panel:user_management')

# Logout view
@login_required
def logout_view(request):
    logout(request)
    return redirect('admin_panel:admin_dashboard')

# Product Dashboard view
@login_required
@user_passes_test(admin_required)
def product_dashboard(request):
    products = Product.objects.all()
    return render(request, 'admin_panel/productdashboard.html', {'products': products})

# Add Product view
@login_required
@user_passes_test(admin_required)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('admin_panel:product_dashboard')
    else:
        form = ProductForm()
    return render(request, 'admin_panel/addproduct.html', {'form': form})

# Edit Product view
@login_required
@user_passes_test(admin_required)
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('admin_panel:product_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin_panel/editproduct.html', {'form': form, 'product': product})

# Delete Product view
@login_required
@user_passes_test(admin_required)
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('admin_panel:product_dashboard')
    return render(request, 'admin_panel/deleteproduct.html', {'product': product})


# Category List view
@login_required
@user_passes_test(admin_required)
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'admin_panel/categorylist.html', {'categories': categories})

# Add Category view
@login_required
@user_passes_test(admin_required)
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_image = request.FILES.get('category_image')  # For handling image files

        if name and not Category.objects.filter(name=name).exists():
            category = Category.objects.create(
                name=name,
                category_image=category_image
            )
            messages.success(request, 'Category added successfully!')
            return redirect('admin_panel:category_list')
        else:
            messages.error(request, 'Category name is required or already exists.')

    return render(request, 'admin_panel/categoryadd.html')

# Edit Category view
@login_required
@user_passes_test(admin_required)
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        category_name = request.POST.get('name')
        image = request.FILES.get('image')

        if category_name:
            category.name = category_name

            # If a new image is uploaded, update it
            if image:
                category.image = image

            category.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('admin_panel:category_list')
        else:
            messages.error(request, 'Category name is required.')

    return render(request, 'admin_panel/categoryedit.html', {'category': category})

# Delete Category view
@login_required
@user_passes_test(admin_required)
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('admin_panel:category_list')
    return render(request, 'admin_panel/categorydelete.html', {'category': category})

# Coupon List view
@login_required
@user_passes_test(admin_required)
def coupon_list(request):
    coupons = Coupon.objects.all()  
    return render(request, 'admin_panel/coupon_list.html', {'coupons': coupons})

# Add Coupon view
@login_required
@user_passes_test(admin_required)
def add_coupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Coupon added successfully!")
            return redirect('admin_panel:coupon_list')  # Redirect to the coupon list page
    else:
        form = CouponForm()

    return render(request, 'admin_panel/add_coupon.html', {'form': form})

# Edit Coupon view
@login_required
@user_passes_test(admin_required)
def edit_coupon(request, coupon_id):
    coupon = Coupon.objects.get(id=coupon_id)
    if request.method == 'POST':
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            messages.success(request, "Coupon updated successfully!")
            return redirect('admin_panel:coupon_list')  # Redirect to the coupon list page
    else:
        form = CouponForm(instance=coupon)

    return render(request, 'admin_panel/edit_coupon.html', {'form': form, 'coupon': coupon})

# Delete Coupon view
@login_required
@user_passes_test(admin_required)
def delete_coupon(request, coupon_id):
    coupon = Coupon.objects.get(id=coupon_id)
    coupon.delete()
    messages.success(request, "Coupon deleted successfully!")
    return redirect('admin_panel:coupon_list')  

@login_required
@user_passes_test(admin_required)
def admin_order(request):
    """
    Display all orders in the admin panel.
    """
    orders = Order.objects.all()  # Fetch all orders
    return render(request, 'admin_panel/admin_order.html', {'orders': orders})


@login_required
@user_passes_test(admin_required)
def admin_update_order_status(request):
    """
    View to update the status of multiple orders.
    """
    if request.method == "POST":
        updated_orders = []  # Correctly use 'updated_orders' here
        for order in Order.objects.all():
            # Get the new status for the current order
            new_status = request.POST.get(f"status_{order.id}")
            
            # Check if the status is different from the current status
            if new_status and new_status != order.status:
                order.status = new_status
                updated_orders.append(order)

        # Bulk update the orders if any status has been changed
        if updated_orders:
            Order.objects.bulk_update(updated_orders, ['status'])
            messages.success(request, "Order statuses updated successfully.")
        else:
            messages.info(request, "No status updates were made.")

        return redirect('admin_panel:admin_order')

    return redirect('admin_panel:admin_order')

def carousel_list(request):
    carousel_items = Carousel.objects.all()
    return render(request, 'admin_panel/carousel_list.html', {'carousel_items': carousel_items})

# View to handle the adding of a carousel item
def add_carousel(request):
    if request.method == 'POST':
        form = CarouselForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:carousel_list')  # Redirect to the carousel list after adding a new item
    else:
        form = CarouselForm()
    return render(request, 'admin_panel/add_carousel.html', {'form': form})

# View to handle the editing of a carousel item
def edit_carousel(request, pk):
    carousel_item = get_object_or_404(Carousel, pk=pk)
    if request.method == 'POST':
        form = CarouselForm(request.POST, request.FILES, instance=carousel_item)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:carousel_list')  # Redirect back to the carousel list after saving
    else:
        form = CarouselForm(instance=carousel_item)
    return render(request, 'admin_panel/edit_carousel.html', {'form': form, 'carousel_item': carousel_item})

# View to handle the deletion of a carousel item
def delete_carousel(request, pk):
    carousel_item = get_object_or_404(Carousel, pk=pk)
    if request.method == 'POST':
        carousel_item.delete()
        return redirect('admin_panel:carousel_list')  # Redirect back to the carousel list after deletion
    return render(request, 'admin_panel/delete_carousel.html', {'carousel_item': carousel_item})