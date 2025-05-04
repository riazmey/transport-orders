
from typing import Tuple
from django.db import transaction
from datetime import datetime

from orders.models import(
    EnumTransportOrderStatus,
    EnumRoutepointAction,
    Marketplace,
    Counterparty,
    TransportOrder,
    TransportOrderTruckReqts,
    TransportOrderExternalID,
    TransportOrderCargo,
    TransportOrderRoutepoint)


class WSMarketplaceBase:

    def __init__(self, market: Marketplace):
        self.market = market
        self.url = market.url
        self.login = market.login
        self.password = market.password
        self.token = market.token

    @transaction.atomic
    def orders_import(self) -> Tuple[list, bool]:
        result = []
        data, success = self.orders_mixin_get()
        if success:
            print(f'get data: {data}')
            for order_data in data:
                result.append(self._order_update_or_create(order_data))
        return result, success

    def orders_mixin_get(self) -> Tuple[list[dict], bool]:
        return [], False

    def _order_update_or_create(self, order_data: dict) -> TransportOrder:
        counterparty = self._counterparty_update_or_create(order_data.get('counterparty'))
        created = order_data.get('created')
        order = self._order_find(order_data, counterparty, created)
        if order:
            order.status = EnumTransportOrderStatus.objects.get(code_str=order_data.get('status'))
            order.currency = order_data.get('currency')
            order.price = order_data.get('price', 0.00)
            order.rate_vat = order_data.get('rate_vat')
            order.save()
        else:
            order = TransportOrder.objects.create(
                market = self.market,
                counterparty = counterparty,
                created = created,
                status = EnumTransportOrderStatus.objects.get(code_str=order_data.get('status')),
                currency = order_data.get('currency'),
                price = order_data.get('price'),
                rate_vat = order_data.get('rate_vat'))
        
        self._order_external_id_create(order, order_data.get('external_id'))
        self._order_cargo_update_or_create(order, order_data.get('cargo'))
        self._order_truck_requirements_update_or_create(order, order_data.get('truck_requirements'))
        self._order_routepoints_update_or_create(order, order_data.get('routepoints'))

        return order

    def _order_find(self, order_data: dict, counterparty: Counterparty, created: datetime) -> TransportOrder | None:
        params_order = {'market': self.market, 'counterparty': counterparty, 'created': created}
        if TransportOrder.objects.filter(**params_order).exists():
            return TransportOrder.objects.get(**params_order)
        else:
            external_id = order_data.get('external_id')
            params_external_id = {'market': self.market, 'external_id': external_id.get('external_id')}
            if TransportOrderExternalID.objects.filter(**params_external_id).exists():
                order_external_id = TransportOrderExternalID.objects.get(**params_external_id)
                return order_external_id.order
            else:
                return None

    def _order_external_id_create(self, order: TransportOrder, external_id_data: dict) -> TransportOrderExternalID:
        TransportOrderExternalID.objects.filter(market=self.market, order=order).delete()
        return TransportOrderExternalID.objects.create(
            market = self.market,
            order = order,
            external_id = external_id_data.get('external_id'),
            external_code = external_id_data.get('external_code'))

    def _counterparty_update_or_create(self, counterparty_data: dict) -> Counterparty:
        inn = counterparty_data.get('inn')
        kpp = counterparty_data.get('kpp')
        counterparty_params = {'inn': inn, 'kpp': kpp}

        if Counterparty.objects.filter(**counterparty_params).exists():
            return Counterparty.objects.get(inn=inn, kpp=kpp)
        else:
            return Counterparty.objects.create(
                inn = inn,
                kpp = kpp,
                name = counterparty_data.get('name'),
                name_full = counterparty_data.get('name_full'))

    def _order_cargo_update_or_create(self, order: TransportOrder, cargo_data: list[dict]) -> list[TransportOrderCargo]:
        result = []
        TransportOrderCargo.objects.filter(order=order).delete()
        for item_data in cargo_data:
            result.append(TransportOrderCargo.objects.create(
                order = order,
                name = item_data.get('name'),
                hazard_class = item_data.get('hazard_class', '0'),
                weight = item_data.get('weight', 0.0),
                weight_unit = item_data.get('weight_unit', ''),
                volume = item_data.get('volume', 0.0),
                volume_unit = item_data.get('volume_unit', '')))
        return result

    def _order_truck_requirements_update_or_create(self, order: TransportOrder, truck_requirements_data: dict) -> TransportOrderTruckReqts:
        TransportOrderTruckReqts.objects.filter(order=order).delete()
        return TransportOrderTruckReqts.objects.create(
            order = order,
            weight = truck_requirements_data.get('weight', 0.0),
            weight_unit = truck_requirements_data.get('weight_unit', ''),
            volume = truck_requirements_data.get('volume', 0.0),
            volume_unit = truck_requirements_data.get('volume_unit', ''),
            refrigeration = truck_requirements_data.get('refrigeration'),
            temperature = truck_requirements_data.get('temperature', 0),
            comment = truck_requirements_data.get('comment', ''))


    def _order_routepoints_update_or_create(self, order: TransportOrder, routepoints_data: list[dict]) -> list[TransportOrderRoutepoint]:
        result = []
        TransportOrderRoutepoint.objects.filter(order=order).delete()
        for item_data in routepoints_data:
            action = EnumRoutepointAction.objects.get(code_str=item_data.get('action'))
            result.append(TransportOrderRoutepoint.objects.create(
                order = order,
                address = item_data.get('address'),
                action = action,
                date_start = item_data.get('date_start'),
                date_end = item_data.get('date_end'),
                counterparty = item_data.get('counterparty', ''),
                contact_person = item_data.get('contact_person', '')))
        return result
