
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.core.cache import cache
from django.db import transaction

from orders.models import Marketplace
from orders.models import TransportOrder
from django.contrib.auth.models import User

from orders.serializers import SerializerTransportOrder
from orders.serializers import SerializerTransportOrderAPIViewParams
from orders.serializers import SerializerTransportOrdersAPIViewParams

from subscriptions.models import Subscription
from subscriptions.models import SubscriptionOrder

from multithreading import MultithreadedDataProcessing


def handler_serialize_transport_orders(data: list, processed_data: list):
    result = SerializerTransportOrder(data, many=True).data
    processed_data.append(result)


class TransportOrderAPIView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def get(self, request: Request) -> dict:

        params = SerializerTransportOrderAPIViewParams(data=request.query_params)
        params.is_valid(raise_exception=True)

        order_obj = TransportOrder.objects.get(id=request.query_params.get('id', ''))

        return Response(SerializerTransportOrder(order_obj).data)


class TransportOrdersAPIView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request: Request):

        if request.query_params.get('direct', '').lower() == 'true':
            direct = True
        else:
            direct = False

        params = SerializerTransportOrdersAPIViewParams(data=request.query_params)
        params.is_valid(raise_exception=True)
        
        market = Marketplace.objects.get(id=request.query_params.get('market'))
        if direct:
            market.ws.orders_import()
        return Response(self._get_serialized_data(market, request))

    @transaction.atomic
    def _get_serialized_data(self, market: Marketplace, request: Request) -> list[dict]:
        key_cache = f'TransportOrdersAPIView._get_serialize_data(market={market.pk})'
        result = cache.get(key_cache)
        if not result:
            result = []
            queryset = []
            user_id = AccessToken(request.auth.token)['user_id']
            user = User.objects.get(id=user_id)
            if Subscription.objects.filter(user=user, model='TransportOrder').exists():
                subscription = Subscription.objects.get(user=user, model='TransportOrder')
                subscription_orders = SubscriptionOrder.objects.filter(subscription=subscription)
                for subscription_order in subscription_orders:
                    queryset.append(subscription_order.order)
            if queryset:
                result = MultithreadedDataProcessing(
                    handler = handler_serialize_transport_orders,
                    data = queryset).processing()
                if result:
                    SubscriptionOrder.objects.filter(subscription=subscription).delete()
                cache.set(key_cache, result, 60 * 60 * 2)
        return result
