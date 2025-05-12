
from django import forms
from subscriptions.models import Subscription


class SubscriptionForm(forms.ModelForm):
    class Meta:

        fields = [
            'user',
            'model']

        model = Subscription
