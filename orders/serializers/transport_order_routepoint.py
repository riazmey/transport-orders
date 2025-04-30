
from rest_framework import serializers
from orders.models import TransportOrderRoutepoint
from.enum_routepoint_action import SerializerEnumRoutepointAction


class SerializerTransportOrderRoutepoint(serializers.Serializer):

    action = SerializerEnumRoutepointAction()

    class Meta:

        fields = (
            'order',
            'action',
            'date',
            'address',
            'counterparty',
            'contact_person',
            'comment',
            'repr')

        model = TransportOrderRoutepoint
