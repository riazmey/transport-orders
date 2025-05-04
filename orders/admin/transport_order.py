
from django.contrib import admin
from orders.forms import TransportOrderForm


class TransportOrderAdmin(admin.ModelAdmin):

    fields = [
        'market',
        ('counterparty', 'status'),
        'modified',
        ('price', 'currency'),
        'rate_vat',
        'comment']

    list_display = [
        'status',
        'modified',
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
        'counterparty',
        'modified',
        'status']

    ordering = [
        'market',
        'counterparty',
        'status',
        'price']

    form = TransportOrderForm
