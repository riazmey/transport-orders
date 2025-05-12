
from django.contrib import admin
from subscriptions.forms import SubscriptionOrderForm


class SubscriptionOrderAdmin(admin.ModelAdmin):

    fields = [
        'subscription',
        'order']

    list_display = [
        'subscription',
        'order']

    ordering = ['subscription']
    form = SubscriptionOrderForm
