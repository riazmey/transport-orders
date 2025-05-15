
# python manage.py shell
# from tasks import registered_all_ordes_to_subscribers
# registered_all_ordes_to_subscribers()

from orders.models import Marketplace
from orders.models import TransportOrder
from subscriptions.models import Subscription
from subscriptions.models import SubscriptionOrder

def orders_import():
    markets = Marketplace.objects.all()
    for market in markets:
        market.ws.orders_import()

def registered_all_ordes_to_subscribers():
    subscriptions = Subscription.objects.all()
    orders = TransportOrder.objects.all()
    for subscription in subscriptions:
        for order in orders:
            SubscriptionOrder.objects.update_or_create(subscription=subscription, order=order)
