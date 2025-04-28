
from django import forms
from django.contrib import admin

from orders.models import TransportOrderTruckReqtsLoadingType


class TransportOrderTruckReqtsLoadingTypeForm(forms.ModelForm):

    class Meta:
        model = TransportOrderTruckReqtsLoadingType
        fields = [
            'order_truck_reqts',
            'loading_type',
        ]


class TransportOrderTruckReqtsLoadingTypeAdmin(admin.ModelAdmin):
    list_display = [
        'order_truck_reqts',
        'loading_type'
    ]
    search_fields = [
        'order_truck_reqts__repr',
        'loading_type__repr'
    ]
    list_filter = [
        'order_truck_reqts',
        'loading_type'
    ]
    ordering = [
        'order_truck_reqts',
        'loading_type'
    ]
    form = TransportOrderTruckReqtsLoadingTypeForm
