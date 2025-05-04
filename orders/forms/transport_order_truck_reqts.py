
from tabnanny import verbose
from django import forms
from orders.models import TransportOrderTruckReqts
from ws.classifiers import WSClassifiers


class TransportOrderTruckReqtsForm(forms.ModelForm):

    ws = WSClassifiers()
    weight_unit = forms.ChoiceField(
        choices = ws.list_units({'type':'weight'}),
        initial = '168'
    )
    volume_unit = forms.ChoiceField(
        choices = ws.list_units({'type':'volume'}),
        initial = '113'
    )

    class Meta:

        fields = [
            'order',
            'weight',
            'weight_unit',
            'volume',
            'volume_unit',
            'refrigeration',
            'temperature',
            'comment']

        widgets = {'comment': forms.Textarea()}
        
        model = TransportOrderTruckReqts
