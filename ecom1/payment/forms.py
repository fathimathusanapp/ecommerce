from django import forms
from payment.models import Order, OrderLine
from decimal import Decimal
import stripe

# Initialize Stripe API key
stripe.api_key = "sk_test_YOUR_SECRET_KEY"

PAYMENT_METHOD_CHOICES = [
    ('cod', 'Cash on Delivery (COD)'),
    ('stripe', 'Stripe'),
]

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_address', 'total_price', 'is_paid', 'payment_method']

    def save(self, commit=True):
        order_instance = super().save(commit=False)
        order_lines = order_instance.order_lines.all()
        total_price = sum(line.get_total() for line in order_lines)
        order_instance.total_price = total_price

        if 'payment_method' in self.cleaned_data:
            order_instance.payment_method = self.cleaned_data['payment_method']
            # Set initial is_paid as False for online payments
            if order_instance.payment_method in [ 'stripe']:
                order_instance.is_paid = False

        if commit:
            order_instance.save()
        return order_instance


class OrderLineForm(forms.ModelForm):
    class Meta:
        model = OrderLine
        fields = ['product', 'quantity', 'unit_price']

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        unit_price = cleaned_data.get('unit_price')

        if quantity <= 0:
            raise forms.ValidationError("Quantity must be a positive number.")

        if unit_price <= Decimal('0.00'):
            raise forms.ValidationError("Unit price must be greater than zero.")

        return cleaned_data


class CheckoutForm(forms.Form):
    # Address Selection
    selected_address = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=[],
        required=False,
        label="Shipping Address",
    )

    # New Address Fields
    new_full_name = forms.CharField(
        required=False,
        label="Full Name",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    new_address = forms.CharField(
        required=False,
        label="Address",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
    )
    new_city = forms.CharField(
        required=False,
        label="City",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    new_postal_code = forms.CharField(
        required=False,
        label="Postal Code",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    new_phone = forms.CharField(
        required=False,
        label="Phone Number",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    # Payment Method Selection
    payment_method = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=PAYMENT_METHOD_CHOICES,
        required=True,
        label="Payment Method",
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.profile.address_set.exists():
            self.fields['selected_address'].choices = [
                (address.id, f"{address.full_name}, {address.address}, {address.city}, {address.postal_code} - Phone: {address.phone}")
                for address in user.profile.address_set.all()
            ]
            self.fields['selected_address'].choices.append(('new', 'Add a new address'))
        else:
            self.fields['selected_address'].choices = [('new', 'Add a new address')]

    def clean(self):
        cleaned_data = super().clean()
        selected_address = cleaned_data.get('selected_address')
        payment_method = cleaned_data.get('payment_method')

        # If 'new' address is selected, validate new address fields
        if selected_address == 'new':
            required_fields = ['new_full_name', 'new_address', 'new_city', 'new_postal_code', 'new_phone']
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, "This field is required for a new address.")

        # Ensure payment method is selected
        if not payment_method:
            self.add_error('payment_method', "Please select a payment method.")

        return cleaned_data
