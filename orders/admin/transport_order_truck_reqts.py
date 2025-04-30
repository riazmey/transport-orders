
from django.contrib import admin
from orders.forms import TransportOrderTruckReqtsForm


class TransportOrderTruckReqtsAdmin(admin.ModelAdmin):
    
    fields = [
        'order',
        ('weight', 'weight_unit'),
        ('volume', 'volume_unit'),
        ('refrigeration', 'temperature'),
        'comment']
    
    list_display = [
        'order',
        'weight',
        'weight_unit',
        'volume',
        'volume_unit',
        'refrigeration',
        'temperature']
    
    search_fields = [
        'order__repr',
        'comment']
    
    list_filter = [
        'order',
        'refrigeration',
        'temperature',
        'weight',
        'volume']

    ordering = ['order']
    form = TransportOrderTruckReqtsForm
