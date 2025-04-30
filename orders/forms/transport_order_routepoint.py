
from django import forms
from orders.models import TransportOrderRoutepoint


class TransportOrderRoutepointForm(forms.ModelForm):

    class Meta:

        fields = [
            'order',
            'action',
            'date_start',
            'date_end',
            'address',
            'counterparty',
            'contact_person',
            'comment']

        widgets = {
            'address': forms.Textarea(),
            'comment': forms.Textarea()}
        
        model = TransportOrderRoutepoint
