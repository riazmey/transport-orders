
from django import forms
from subscriptions.models import SubscriptionOrder


class SubscriptionOrderForm(forms.ModelForm):
    class Meta:

        fields = [
            'subscription',
            'order']

        model = SubscriptionOrder
