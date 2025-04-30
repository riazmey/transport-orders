
from django import forms
from orders.models import TransportOrderTruckReqtsLoadingType


class TransportOrderTruckReqtsLoadingTypeForm(forms.ModelForm):

    class Meta:

        fields = [
            'order_truck_reqts',
            'loading_type']

        model = TransportOrderTruckReqtsLoadingType