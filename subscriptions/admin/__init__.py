
from django.contrib import admin

from subscriptions.models import (
    Subscription,
    SubscriptionOrder)

from .subscription import SubscriptionAdmin
from .subscription_order import SubscriptionOrderAdmin


admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(SubscriptionOrder, SubscriptionOrderAdmin)
