from django import forms
from .models import ShopCard


class ShopCardForm(forms.ModelForm):

    class Meta:
        model = ShopCard
        fields = ['quantity']
        