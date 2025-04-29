
from django import forms
from orders.models import Marketplace


class MarketplaceForm(forms.ModelForm):
    class Meta:
        model = Marketplace
        fields = [
            'type',
            'url',
            'login',
            'password',
            'token'
        ]
        widgets = {
            'url': forms.URLInput(),
            'password': forms.PasswordInput(),
            'token': forms.PasswordInput()
        }
