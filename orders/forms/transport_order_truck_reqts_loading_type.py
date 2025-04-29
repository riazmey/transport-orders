
from django import forms
from orders.models import TransportOrderTruckReqtsLoadingType


class TransportOrderTruckReqtsLoadingTypeForm(forms.ModelForm):

    class Meta:
        model = TransportOrderTruckReqtsLoadingType
        fields = [
            'order_truck_reqts',
            'loading_type',
        ]
