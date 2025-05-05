
from rest_framework import serializers
from orders.models import TransportOrderExternalID

from .marketplace import SerializerMarketplace


class SerializerTransportOrderExternalID(serializers.ModelSerializer):

    market = SerializerMarketplace()

    class Meta:

        fields = (
            'market',
            'external_id',
            'external_code')

        model = TransportOrderExternalID
 