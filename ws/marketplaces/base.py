
from django.db import transaction


class WSMarketplaceBase:

    def __init__(self, market):
        self.market = market
        self.url = market.url
        self.login = market.login
        self.password = market.password

    @transaction.atomic
    def order_import(self, **kwargs) -> (list[dict] | bool):
        result = []
        data, success = self.order_get(**kwargs)
        if success:
            for order_data in data:
                result += self._order_import(**order_data)
        return result, success

    def _order_import(self, **kwargs) -> list[dict]:
        result = []
        return result

    def order_get(self) -> (list[dict] | bool):
        return [], False
