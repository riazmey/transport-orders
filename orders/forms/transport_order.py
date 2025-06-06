
from django import forms
from orders.models import TransportOrder
from ws.classifiers import WSClassifiers


class TransportOrderForm(forms.ModelForm):

    ws = WSClassifiers()

    currency = forms.ChoiceField(
        choices = ws.list_currencies(),
        initial = 'RUB')

    rate_vat = forms.ChoiceField(
        choices = ws.list_rates_vat(),
        initial = 'with_vat20')

    class Meta:
        
        fields = [
            'counterparty',
            'modified',
            'status',
            'price',
            'currency',
            'rate_vat',
            'comment']
        
        widgets = {'comment': forms.Textarea()}
        model = TransportOrder
