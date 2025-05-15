
from rest_framework import serializers
from orders.models import TransportOrderCargo
from ws.classifiers import WSClassifiers


class SerializerTransportOrderCargo(serializers.ModelSerializer):

    weight_unit = serializers.SerializerMethodField()
    volume_unit = serializers.SerializerMethodField()

    def get_weight_unit(self, data) -> dict:
        data_unit = WSClassifiers().get_unit({'code_dec': data.weight_unit})
        if data_unit:
            return data_unit[0]
        else:
            return {}

    def get_volume_unit(self, data) -> dict:
        data_unit = WSClassifiers().get_unit({'code_dec': data.volume_unit})
        if data_unit:
            return data_unit[0]
        else:
            return {}

    class Meta:

        fields = (
            'name',
            'hazard_class',
            'weight',
            'weight_unit',
            'volume',
            'volume_unit',
            'comment',
            'repr')

        model = TransportOrderCargo
