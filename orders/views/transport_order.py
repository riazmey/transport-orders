
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import TransportOrder
from orders.serializers import SerializerTransportOrder
from orders.serializers import SerializerTransportOrderAPIViewParams


class TransportOrderAPIView(APIView):

    def get(self, request) -> dict:

        params = SerializerTransportOrderAPIViewParams(data=request.query_params)
        params.is_valid(raise_exception=True)

        order_obj = TransportOrder.objects.get(id=request.query_params.get('id', ''))
        return Response(SerializerTransportOrder(order_obj).data)

class TransportOrdersAPIView(APIView):

    def get(self, request) -> dict:

        params = SerializerTransportOrderAPIViewParams(data=request.query_params)
        params.is_valid(raise_exception=True)

        order_obj = TransportOrder.objects.get(id=request.query_params.get('id', ''))
        return Response(SerializerTransportOrder(order_obj).data)