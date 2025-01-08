from django import forms
from decimal import Decimal
from .models import Product
from home.models import Cart, Wishlist, WishlistItem, Coupon 


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 'image']


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['product', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Restrict the quantity to a maximum value, if necessary
        self.fields['quantity'].widget.attrs.update({'min': 1})  # You can set a max limit if needed


class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['user']

    def __init__(self, *args, **kwargs):
        user = kwargs.get('user')  # Fetch logged-in user from view
        super().__init__(*args, **kwargs)
        if user:
            self.fields['user'].initial = user  # Pre-fill the user field with the logged-in user


class WishlistItemForm(forms.ModelForm):
    class Meta:
        model = WishlistItem
        fields = ['wishlist', 'product']




class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code']

    def clean_code(self):
        code = self.cleaned_data.get('code')
        # Validate if coupon exists or is active
        if not Coupon.objects.filter(code=code, active=True).exists():
            raise forms.ValidationError("Invalid or inactive coupon code.")
        return code



