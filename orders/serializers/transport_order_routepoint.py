
from rest_framework import serializers
from orders.models import TransportOrderRoutepoint
from.enum_routepoint_action import SerializerEnumRoutepointAction


class SerializerTransportOrderRoutepoint(serializers.ModelSerializer):

    action = SerializerEnumRoutepointAction()

    class Meta:

        fields = (
            'action',
            'date_start',
            'date_end',
            'address',
            'counterparty',
            'contact_person',
            'comment',
            'repr')

        model = TransportOrderRoutepoint
