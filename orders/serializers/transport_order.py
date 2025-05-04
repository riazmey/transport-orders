
from rest_framework import serializers
from orders.models import TransportOrder
from orders.validators import validate_transport_order_id

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

    class Meta:

        fields = (
            'id',
            'market',
            'counterparty',
            'created',
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
