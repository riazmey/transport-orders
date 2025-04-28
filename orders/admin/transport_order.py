
from django import forms
from django.contrib import admin

from orders.models import TransportOrder


class TransportOrderForm(forms.ModelForm):
    class Meta:
        model = TransportOrder
        fields = [
            'market',
            'status',
            'counterparty',
            'price',
            'currency',
            'rate_vat',
            'comment'
        ]
        widgets = {
            'comment': forms.Textarea(),
        }


class TransportOrderAdmin(admin.ModelAdmin):
    fields = [
        ('market', 'status'),
        'counterparty',
        ('price', 'currency'),
        'rate_vat',
        'comment'
    ]
    list_display = [
        'market',
        'status',
        'counterparty',
        'price',
        'currency',
        'rate_vat'
    ]
    search_fields = [
        'id',
        'counterparty__repr',
        'price'
    ]
    list_filter = [
        'market',
        'status',
        'counterparty'
    ]
    ordering = [
        'market',
        'status',
        'currency',
        'price'
    ]
    form = TransportOrderForm
