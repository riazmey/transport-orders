
from django.contrib import admin
from orders.forms import CounterpartyForm


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
