
from django.contrib import admin
from orders.forms import TransportOrderCargoForm


class TransportOrderCargoAdmin(admin.ModelAdmin):
    fields = [
        'order',
        'name',
        ('weight', 'weight_unit'),
        ('volume', 'volume_unit'),
        'comment'
    ]
    list_display = [
        'order',
        'name',
        'weight',
        'weight_unit',
        'volume',
        'volume_unit'
    ]
    search_fields = [
        'name',
        'order__repr'
    ]
    list_filter = [
        'order',
        'name'
    ]
    ordering = [
        'order',
        'name'
    ]
    form = TransportOrderCargoForm
