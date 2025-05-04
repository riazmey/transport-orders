
from rest_framework import serializers
from orders.models import TransportOrderTruckReqts
from .transport_order_truck_reqts_loading_type import SerializerTransportOrderTruckReqtsLoadingType


class SerializerTransportOrderTruckReqts(serializers.ModelSerializer):

    loading_types = SerializerTransportOrderTruckReqtsLoadingType(
        many = True,
        source = 'order_truck_reqts_relate_order_truck_reqts_loading_type')

    class Meta:

        fields = (
            'weight',
            'weight_unit',
            'volume',
            'volume_unit',
            'refrigeration',
            'temperature',
            'loading_types',
            'comment',
            'repr')
        
        model = TransportOrderTruckReqts
