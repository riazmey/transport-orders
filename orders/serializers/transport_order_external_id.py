
from rest_framework import serializers
from orders.models import TransportOrderExternalID


class SerializerTransportOrderExternalID(serializers.ModelSerializer):

    class Meta:

        fields = (
            'external_id',
            'external_code')

        model = TransportOrderExternalID
 