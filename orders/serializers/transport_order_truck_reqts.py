
from rest_framework import serializers
from orders.models import TransportOrderTruckReqts
from ws.classifiers import WSClassifiers

from .transport_order_truck_reqts_loading_type import SerializerTransportOrderTruckReqtsLoadingType


class SerializerTransportOrderTruckReqts(serializers.ModelSerializer):

    loading_types = SerializerTransportOrderTruckReqtsLoadingType(
        many = True,
        source = 'order_truck_reqts_relate_order_truck_reqts_loading_type')

    weight_unit = serializers.SerializerMethodField()
    volume_unit = serializers.SerializerMethodField()

    def get_weight_unit(self, data) -> dict:
        data_unit, recieved = WSClassifiers().get_unit({'code_dec': data.weight_unit})
        if recieved:
            return data_unit
        else:
            return {}

    def get_volume_unit(self, data) -> dict:
        data_unit, recieved = WSClassifiers().get_unit({'code_dec': data.volume_unit})
        if recieved:
            return data_unit
        else:
            return {}

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
