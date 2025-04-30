
from rest_framework import serializers
from orders.models import Marketplace


class SerializerMarketplace(serializers.Serializer):

    class Meta:

        fields = (
            'id',
            'url',
            'login',
            'repr')

        model = Marketplace
