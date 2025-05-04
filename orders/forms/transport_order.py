
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
        initial = 'RUB')

    class Meta:
        
        fields = [
            'counterparty',
            'created',
            'status',
            'price',
            'currency',
            'rate_vat',
            'comment']
        
        widgets = {'comment': forms.Textarea()}
        model = TransportOrder
