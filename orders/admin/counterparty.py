
from django import forms
from django.contrib import admin

from orders.models import Counterparty


class CounterpartyForm(forms.ModelForm):
    class Meta:
        model = Counterparty
        fields = [
            'name',
            'name_full',
            'inn',
            'kpp'
        ]


class CounterpartyAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'name_full',
        ('inn', 'kpp')
    ]
    list_display = [
        'name',
        'name_full',
        'inn',
        'kpp'
    ]
    search_fields = [
        'name',
        'inn'
    ]
    ordering = ['name']
    form = CounterpartyForm
