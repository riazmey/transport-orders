
from rest_framework import serializers
from orders.models import Marketplace


class SerializerMarketplace(serializers.ModelSerializer):

    class Meta:

        fields = (
            'id',
            'url',
            'login',
            'repr')

        model = Marketplace
