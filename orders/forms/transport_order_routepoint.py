
from django import forms
from orders.models import TransportOrderRoutepoint


class TransportOrderRoutepointForm(forms.ModelForm):

    class Meta:
        model = TransportOrderRoutepoint
        fields = [
            'order',
            'action',
            'date',
            'address',
            'counterparty',
            'contact_person',
            'comment'
        ]
        widgets = {
            'address': forms.Textarea(),
            'comment': forms.Textarea(),
        }
