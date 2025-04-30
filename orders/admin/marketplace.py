
from django.contrib import admin
from orders.forms import MarketplaceForm


class MarketplaceAdmin(admin.ModelAdmin):

    fields = [
        'type',
        'url',
        'login',
        'password',
        'token']

    list_display = [
        'type',
        'url',
        'login']

    search_fields = [
        'url',
        'login']

    list_filter = ['type']
    ordering = ['type']
    form = MarketplaceForm
