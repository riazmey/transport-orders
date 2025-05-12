
from django.contrib import admin
from subscriptions.forms import SubscriptionForm


class SubscriptionAdmin(admin.ModelAdmin):

    fields = [
        'user',
        'model']

    list_display = [
        'user',
        'model']

    ordering = ['user']
    form = SubscriptionForm
