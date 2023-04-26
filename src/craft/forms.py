from django import forms

from craft.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["product", "quantity"]


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["buyer_name", "buyer_phonenumber", "shipping_address", "payment_method"]
