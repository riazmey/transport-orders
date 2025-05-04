
from rest_framework import serializers
from orders.models import EnumMarketplaceType


class SerializerEnumMarketplaceType(serializers.ModelSerializer):
    
    class Meta:

        fields = (
            'code_str',
            'repr')

        model = EnumMarketplaceType
