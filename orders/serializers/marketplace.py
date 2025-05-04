
from rest_framework import serializers
from orders.models import Marketplace
from orders.validators import validate_marketplace_id

from .enum_marketplace_type import SerializerEnumMarketplaceType


class SerializerMarketplace(serializers.ModelSerializer):

    type = SerializerEnumMarketplaceType()

    class Meta:

        fields = (
            'id',
            'type',
            'url',
            'login',
            'repr')

        model = Marketplace

class SerializerMarketplaceAPIViewParams(serializers.Serializer):
    id = serializers.IntegerField(validators=[validate_marketplace_id])