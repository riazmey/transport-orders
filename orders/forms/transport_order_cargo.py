
from django import forms
from orders.models import TransportOrderCargo
from ws import WSClassifiers


class TransportOrderCargoForm(forms.ModelForm):

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
        model = TransportOrderCargo
        fields = [
            'order',
            'name',
            'weight',
            'weight_unit',
            'volume',
            'volume_unit',
            'comment'
        ]
        widgets = {
            'comment': forms.Textarea(),
        }
