
from rest_framework import serializers
from orders.models import Marketplace


class SerializerMarketplace(serializers.Serializer):

    class Meta:
        model = Marketplace
        fields = (
            'id',
            'url',
            'login',
            'repr'
        )
