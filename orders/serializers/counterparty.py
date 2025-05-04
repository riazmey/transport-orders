
from rest_framework import serializers  
from orders.models import Counterparty


class SerializerCounterparty(serializers.ModelSerializer):

    class Meta:

        fields = (
            'id',
            'name',
            'name_full',
            'inn',
            'kpp',
            'repr')

        model = Counterparty
