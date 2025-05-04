
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from orders.models import Marketplace
from orders.models import TransportOrder
from orders.serializers import SerializerTransportOrder
from orders.serializers import SerializerTransportOrderAPIViewParams
from orders.serializers import SerializerTransportOrdersAPIViewParams


class TransportOrderAPIView(APIView):

    def get(self, request) -> dict:

        params = SerializerTransportOrderAPIViewParams(data=request.query_params)
        params.is_valid(raise_exception=True)

        order_obj = TransportOrder.objects.get(id=request.query_params.get('id', ''))
        return Response(SerializerTransportOrder(order_obj).data)

class TransportOrdersAPIView(APIView):

    def get(self, request):

        if request.query_params.get('direct', '').lower() == 'true':
            direct = True
        else:
            direct = False

        params = SerializerTransportOrdersAPIViewParams(data=request.query_params)
        params.is_valid(raise_exception=True)

        market = Marketplace.objects.get(id=request.query_params.get('market'))
        if direct:
            market.ws.orders_import()

        queryset = TransportOrder.objects.filter(market=market)

        if queryset:
            return Response(SerializerTransportOrder(queryset, many=True).data)
        else:
            message = 'Couldn\'t find a transport orders'
            raise serializers.ValidationError(message)