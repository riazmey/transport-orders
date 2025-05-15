
from rest_framework import serializers
from orders.models import TransportOrder
from orders.validators import validate_transport_order_id
from orders.validators import validate_transport_order_market
from ws.classifiers import WSClassifiers

from .enum_transport_order_status import SerializerEnumTransportOrderStatus
from .marketplace import SerializerMarketplace
from .counterparty import SerializerCounterparty
from .transport_order_cargo import SerializerTransportOrderCargo
from .transport_order_routepoint import SerializerTransportOrderRoutepoint
from .transport_order_truck_reqts import SerializerTransportOrderTruckReqts
from .transport_order_external_id import SerializerTransportOrderExternalID


class SerializerTransportOrder(serializers.ModelSerializer):

    market = SerializerMarketplace()
    counterparty = SerializerCounterparty()
    status = SerializerEnumTransportOrderStatus()
    cargo = SerializerTransportOrderCargo(many = True, source = 'order_relate_cargo')
    routepoints = SerializerTransportOrderRoutepoint(many = True, source = 'order_relate_routepoint')
    external_ids = SerializerTransportOrderExternalID(many = True, source = 'order_relate_external_id')
    truck_requirements = SerializerTransportOrderTruckReqts(many = False, source = 'order_relate_truck_requirements')
    currency = serializers.SerializerMethodField()
    rate_vat = serializers.SerializerMethodField()

    def get_currency(self, data) -> dict:
        data_currency = WSClassifiers().get_currency({'code_str': data.currency})
        if data_currency:
            return data_currency[0]
        else:
            return {}

    def get_rate_vat(self, data) -> dict:
        data_rate_vat = WSClassifiers().get_rate_vat({'code_str': data.rate_vat})
        if data_rate_vat:
            return data_rate_vat[0]
        else:
            return {}

    class Meta:

        fields = (
            'id',
            'market',
            'counterparty',
            'modified',
            'status',
            'cargo',
            'routepoints',
            'external_ids',
            'truck_requirements',
            'currency',
            'price',
            'rate_vat',
            'comment',
            'repr')

        model = TransportOrder

class SerializerTransportOrderAPIViewParams(serializers.Serializer):
    id = serializers.CharField(validators=[validate_transport_order_id])

class SerializerTransportOrdersAPIViewParams(serializers.Serializer):
    market = serializers.CharField(validators=[validate_transport_order_market])
