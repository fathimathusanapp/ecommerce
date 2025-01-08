from django import forms
from .models import Address

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Address  # Use Address model since Profile is now merged into Address
        fields = ['first_name', 'last_name', 'phone_number', 'housename', 'street', 'city', 'state', 'zipcode']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'phone_number', 'housename', 'street', 'city', 'state', 'zipcode']

    def clean_zipcode(self):
        zipcode = self.cleaned_data.get('zipcode')
        if len(zipcode) != 6:
            raise forms.ValidationError("Zipcode must be 6 digits.")
        return zipcode
    
from django.contrib.auth.forms import PasswordResetForm as DjangoPasswordResetForm

class CustomSetPasswordForm(forms.Form):
    new_password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

