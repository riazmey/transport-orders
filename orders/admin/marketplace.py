
from django import forms
from django.contrib import admin

from orders.models import Marketplace


class MarketplaceForm(forms.ModelForm):
    class Meta:
        model = Marketplace
        fields = [
            'type',
            'url',
            'login',
            'password'
        ]
        widgets = {
            'url': forms.URLInput(),
            'password': forms.PasswordInput()
        }


class MarketplaceAdmin(admin.ModelAdmin):
    fields = [
        'type',
        'url',
        'login',
        'password'
    ]
    list_display = [
        'type',
        'login'
    ]
    search_fields = [
        'url',
        'type__repr'
    ]
    ordering = ['type']
    form = MarketplaceForm
