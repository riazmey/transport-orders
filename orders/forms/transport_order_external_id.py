
from django import forms
from orders.models import TransportOrderExternalID


class TransportOrderExternalIDForm(forms.ModelForm):

    class Meta:

        fields = [
            'market',
            'order',
            'external_id',
            'external_code']

        model = TransportOrderExternalID
