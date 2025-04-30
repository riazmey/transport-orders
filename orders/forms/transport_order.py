
from django import forms
from orders.models import TransportOrder


class TransportOrderForm(forms.ModelForm):
    class Meta:
        
        fields = [
            'market',
            'status',
            'created',
            'counterparty',
            'price',
            'currency',
            'rate_vat',
            'comment']
        
        widgets = {'comment': forms.Textarea()}
        model = TransportOrder
