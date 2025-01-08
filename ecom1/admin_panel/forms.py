from django import forms
from home.models import Category, Product
from home.models import Coupon
from account.forms import  AddressForm
from account.models import Address
from home.models import Carousel


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'category_image']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 'image']
        
class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'discount_percentage', 'active']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['first_name', 'last_name','phone_number','housename', 'street', 'city', 'state', 'zipcode']
        
    address = AddressForm()  


class CarouselForm(forms.ModelForm):
    class Meta:
        model = Carousel
        fields = ['title', 'description', 'image', 'order', 'active']  # Fields to include in the form

    title = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Title'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Description'}))
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    order = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Display Order'}))
    active = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))



    
