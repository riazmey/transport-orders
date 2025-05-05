
from django import forms
from orders.models import TransportOrderCargo
from ws.classifiers import WSClassifiers


class TransportOrderCargoForm(forms.ModelForm):

    ws = WSClassifiers()
    
    weight_unit = forms.ChoiceField(
        choices = ws.list_units({'type':'weight'}),
        initial = '168')
    
    volume_unit = forms.ChoiceField(
        choices = ws.list_units({'type':'volume'}),
        initial = '113')

    hazard_class = forms.ChoiceField(
        choices = ws.list_cargos_hazards(),
        initial = '0')

    class Meta:

        fields = [
            'order',
            'name',
            'hazard_class',
            'weight',
            'weight_unit',
            'volume',
            'volume_unit',
            'comment']

        widgets = {'comment': forms.Textarea()}
        
        model = TransportOrderCargo
