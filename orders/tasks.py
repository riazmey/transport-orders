
from orders.models import Marketplace

def orders_import():
    markets = Marketplace.objects.all()
    for market in markets:
        market.ws.orders_import()
