
from django.db import transaction
from typing import Any, Dict, Tuple


class WSMarketplaceBase:

    def __init__(self, market):
        self.market = market
        self.url = market.url
        self.login = market.login
        self.password = market.password
        self.token = market.token

    @transaction.atomic
    def orders_import(self) -> Tuple[list, bool]:
        result = []
        data, success = self.orders_get()
        if success:
            for order_data in data:
                result += self._order_import(**order_data)
        return result, success

    def _order_import(self, **kwargs) -> list[dict]:
        result = []
        return result

    def orders_get(self) -> Tuple[Any, bool]:
        return [], False
