
from django import forms
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
