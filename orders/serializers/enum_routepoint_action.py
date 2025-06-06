
from rest_framework import serializers
from orders.models import EnumRoutepointAction


class SerializerEnumRoutepointAction(serializers.ModelSerializer):
    
    class Meta:

        fields = (
            'code_str',
            'repr')

        model = EnumRoutepointAction
