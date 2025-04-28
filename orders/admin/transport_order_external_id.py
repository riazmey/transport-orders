
from django import forms
from django.contrib import admin

from orders.models import TransportOrderExternalID


class TransportOrderExternalIDForm(forms.ModelForm):

    class Meta:
        model = TransportOrderExternalID
        fields = [
            'market',
            'order',
            'external_id',
            'external_code'
        ]


class TransportOrderExternalIDAdmin(admin.ModelAdmin):
    fields = [
        'market',
        'order',
        ('external_id', 'external_code')
    ]
    list_display = [
        'market',
        'order',
        'external_id',
        'external_code'
    ]
    search_fields = [
        'external_id',
        'external_code'
    ]
    list_filter = [
        'market',
        'order'
    ]
    ordering = [
        'market',
        'order'
    ]
    form = TransportOrderExternalIDForm
