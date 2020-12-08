from django import forms
from .models import ShopCard, Order


class ShopCardForm(forms.ModelForm):

    class Meta:
        model = ShopCard
        fields = ['quantity']
        

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'address', 'phone','city', 'country']
        