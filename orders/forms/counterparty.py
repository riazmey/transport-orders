
from django import forms
from orders.models import Counterparty


class CounterpartyForm(forms.ModelForm):
    class Meta:

        fields = [
            'name',
            'name_full',
            'inn',
            'kpp']

        model = Counterparty
