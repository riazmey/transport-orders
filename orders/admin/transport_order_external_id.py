

from django.contrib import admin
from orders.forms import TransportOrderExternalIDForm


class TransportOrderExternalIDAdmin(admin.ModelAdmin):
    
    fields = [
        'market',
        'order',
        ('external_id', 'external_code')]
    
    list_display = [
        'market',
        'order',
        'external_id',
        'external_code']
    
    search_fields = [
        'external_id',
        'external_code']
    
    list_filter = [
        'market',
        'order']
    
    ordering = [
        'market',
        'order']
    
    form = TransportOrderExternalIDForm
