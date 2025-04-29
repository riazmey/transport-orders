
from rest_framework import serializers  
from orders.models import Counterparty


class SerializerCounterparty(serializers.Serializer):

    class Meta:
        model = Counterparty
        fields = (
            'id',
            'name',
            'name_full',
            'inn',
            'kpp',
            'repr'
        )