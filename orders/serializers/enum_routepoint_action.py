
from rest_framework import serializers
from orders.models import EnumRoutepointAction


class SerializerEnumRoutepointAction(serializers.Serializer):
    
    class Meta:
        model = EnumRoutepointAction
        fields = (
            'code_str',
            'repr'
        )
