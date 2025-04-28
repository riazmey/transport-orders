
from django import forms
from django.contrib import admin

from orders.models import TransportOrderTruckReqts
from ws import WSClassifiers


def list_units(params: dict):
    result = []
    units, success = WSClassifiers().get_units(params)
    if success:
        for unit_data in units:
            result.append((unit_data.code_str, unit_data.name))
    return result

class TransportOrderTruckReqtsForm(forms.ModelForm):

    weight_unit = forms.ChoiceField(choices=list_units({'type':'weight'}))
    volume_unit = forms.ChoiceField(choices=list_units({'type':'volume'}))

    class Meta:
        model = TransportOrderTruckReqts
        fields = [
            'order',
            'weight',
            'weight_unit',
            'volume',
            'volume_unit',
            'refrigeration',
            'temperature',
            'comment'
        ]
        widgets = {
            'comment': forms.Textarea(),
        }


class TransportOrderTruckReqtsAdmin(admin.ModelAdmin):
    fields = [
        'order',
        ('weight', 'weight_unit'),
        ('volume', 'volume_unit'),
        ('refrigeration', 'temperature'),
        'comment'
    ]
    list_display = [
        'order',
        'weight',
        'weight_unit',
        'volume',
        'volume_unit',
        'refrigeration',
        'temperature'
    ]
    search_fields = [
        'order__repr',
        'comment'
    ]
    list_filter = [
        'order',
        'refrigeration',
        'temperature',
        'weight',
        'volume'
    ]
    ordering = ['order']
    form = TransportOrderTruckReqtsForm
