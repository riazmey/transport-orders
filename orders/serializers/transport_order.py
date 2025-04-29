
from rest_framework import serializers
from orders.models import TransportOrder
from orders.validators import validate_transport_order_id

from .enum_transport_order_status import SerializerEnumTransportOrderStatus
from .marketplace import SerializerMarketplace
from .counterparty import SerializerCounterparty
from .transport_order_cargo import SerializerTransportOrderCargo
from .transport_order_routepoint import SerializerTransportOrderRoutepoint
from .transport_order_truck_reqts import SerializerTransportOrderTruckReqts


class SerializerTransportOrder(serializers.ModelSerializer):
    market = SerializerMarketplace()
    status = SerializerEnumTransportOrderStatus()
    counterparty = SerializerCounterparty()
    cargo = SerializerTransportOrderCargo(many=True)
    routepoints = SerializerTransportOrderRoutepoint(many=True)
    truck_requirements = SerializerTransportOrderTruckReqts()

    class Meta:  
        model = TransportOrder 
        fields = (
            'market',
            'status',
            'created',
            'counterparty',
            'cargo',
            'routepoints',
            'truck_requirements',
            'currency',
            'price',
            'rate_vat',
            'comment',
            'repr'
        )

class TransportOrderAPIViewSerializerParams(serializers.Serializer):
    id = serializers.CharField(validators=[validate_transport_order_id])
