
from django.contrib import admin
from orders.forms import TransportOrderRoutepointForm


class TransportOrderRoutepointAdmin(admin.ModelAdmin):
    fields = [
        'order',
        ('action', 'date'),
        'address',
        'counterparty',
        'contact_person',
        'comment'
    ]
    list_display = [
        'order',
        'action',
        'date',
        'address',
        'counterparty',
        'contact_person'
    ]
    search_fields = [
        'order',
        'address',
        'date',
        'counterparty',
        'contact_person'
    ]
    list_filter = [
        'order',
        'action'
    ]
    ordering = [
        'order',
        'action',
        'address'
    ]
    form = TransportOrderRoutepointForm
