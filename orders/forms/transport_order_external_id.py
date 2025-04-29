
from django import forms
from orders.models import TransportOrderExternalID


class TransportOrderExternalIDForm(forms.ModelForm):

    class Meta:
        model = TransportOrderExternalID
        fields = [
            'market',
            'order',
            'external_id',
            'external_code'
        ]
