
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from orders.models import Marketplace
from orders.serializers import SerializerMarketplace
from orders.serializers import SerializerMarketplaceAPIViewParams


class MarketplaceAPIView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request) -> dict:

        params = SerializerMarketplaceAPIViewParams(data=request.query_params)
        params.is_valid(raise_exception=True)

        order_obj = Marketplace.objects.get(id=request.query_params.get('id', ''))
        return Response(SerializerMarketplace(order_obj).data)
