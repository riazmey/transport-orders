
from django import forms
from django.contrib import admin

from orders.models import TransportOrderCargo
from ws import WSClassifiers


def list_units(params: dict):
    result = []
    units, success = WSClassifiers().get_units(params)
    if success:
        for unit_data in units:
            result.append((unit_data.code_str, unit_data.name))
    return result


class TransportOrderCargoForm(forms.ModelForm):

    weight_unit = forms.ChoiceField(choices=list_units({'type':'weight'}))
    volume_unit = forms.ChoiceField(choices=list_units({'type':'volume'}))

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


class TransportOrderCargoAdmin(admin.ModelAdmin):
    fields = [
        'order',
        'name',
        ('weight', 'weight_unit'),
        ('volume', 'volume_unit'),
        'comment'
    ]
    list_display = [
        'order',
        'name',
        'weight',
        'weight_unit',
        'volume',
        'volume_unit'
    ]
    search_fields = [
        'name',
        'order__repr'
    ]
    list_filter = [
        'order',
        'name'
    ]
    ordering = [
        'order',
        'name'
    ]
    form = TransportOrderCargoForm
