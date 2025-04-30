
from django.contrib import admin
from orders.forms import TransportOrderForm


class TransportOrderAdmin(admin.ModelAdmin):

    fields = [
        ('market', 'status'),
        'created',
        'counterparty',
        ('price', 'currency'),
        'rate_vat',
        'comment']

    list_display = [
        'market',
        'status',
        'created',
        'counterparty',
        'price',
        'currency',
        'rate_vat']

    search_fields = [
        'id',
        'counterparty__repr',
        'price']

    list_filter = [
        'market',
        'status',
        'created',
        'counterparty']

    ordering = [
        'market',
        'status',
        'currency',
        'price']

    form = TransportOrderForm
