from django import forms

from craft.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["name", "product", "status", "quantity"]
