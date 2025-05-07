
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.core.cache import cache

from orders.models import Marketplace
from orders.models import TransportOrder
from orders.serializers import SerializerTransportOrder
from orders.serializers import SerializerTransportOrderAPIViewParams
from orders.serializers import SerializerTransportOrdersAPIViewParams

from orders.multithreading import MultithreadedDataProcessing


def handler_serialize_transport_orders(data: list, queue):
    result = SerializerTransportOrder(data, many=True).data
    queue.put(result)

class TransportOrderAPIView(APIView):

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
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
        return Response(self._get_serialized_data(market))

    def _get_serialized_data(self, market: Marketplace) -> list[dict]:
        key_cache = f'TransportOrdersAPIView._get_serialize_data(market={market.pk})'
        result = cache.get(key_cache)
        if result:
            return result
        else:
            queryset = TransportOrder.objects.filter(market=market)
            if queryset:
                result = MultithreadedDataProcessing(
                    handler = handler_serialize_transport_orders,
                    data = queryset).processing()
                cache.set(key_cache, result, 60 * 60 * 2)
                return result
            else:
                message = 'Couldn\'t find a transport orders'
                raise serializers.ValidationError(message)