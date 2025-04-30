from django.db import transaction
from typing import Tuple

from .enum_transport_order_status import EnumTransportOrderStatus
from .counterparty import Counterparty
from .transport_order import TransportOrder
from .transport_order_truck_reqts import TransportOrderTruckReqts
from .transport_order_external_id import TransportOrderExternalID
from .transport_order_cargo import TransportOrderCargo
from .transport_order_routepoint import TransportOrderRoutepoint


class MarketplaceBaseWS:

    def __init__(self, market):
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
            for order_data in data:
                result += self._order_update_or_create(order_data)
        return result, success

    def orders_mixin_get(self) -> Tuple[list[dict], bool]:
        return [], False

    def _order_update_or_create(self, order_data: dict) -> TransportOrder:
        
        external_id = order_data.get('external_id')
        order_external_id = TransportOrderExternalID.objects.get(
            market = self.market,
            external_id = external_id.get('external_id'))
        if order_external_id:
            order = self._order_update(order_external_id, order_data)
        else:
            order = self._order_create(order_data)
            self._order_external_id_create(order, external_id)
        
        self._order_cargo_update_or_create(order, order_data.get('cargo'))
        self._order_truck_requirements_update_or_create(order, order_data.get('truck_requirements'))
        self._order_routepoints_update_or_create(order, order_data.get('routepoints'))

        return order

    def _order_update(self, order: TransportOrder, order_data: dict) -> TransportOrder:
        order.market = self.market
        order.status = EnumTransportOrderStatus.objects.get(code_str=order_data.get('status'))
        order.counterparty = self._counterparty_update_or_create(order_data.get('counterparty'))
        order.currency = order_data.get('currency'),
        order.price = order_data.get('price'),
        order.rate_vat = order_data.get('rate_vat'),
        order.comment = order_data.get('comment'),
        order.save()
        return order

    def _order_create(self, order_data: dict) -> TransportOrder:
        return TransportOrder.objects.create(
            market = self.market,
            created = order_data.get('created'),
            status = EnumTransportOrderStatus.objects.get(code_str=order_data.get('status')),
            counterparty = self._counterparty_update_or_create(order_data.get('counterparty')),
            currency = order_data.get('currency'),
            price = order_data.get('price'),
            rate_vat = order_data.get('rate_vat'),
            comment = order_data.get('comment'),
        )

    def _order_external_id_create(self, order: TransportOrder, external_id_data: dict) -> TransportOrderExternalID:
        return TransportOrderExternalID.objects.create(
            market = self.market,
            order = order,
            external_id = external_id_data.get('external_id'),
            external_code = external_id_data.get('external_code'))

    def _counterparty_update_or_create(self, counterparty_data: dict) -> Counterparty:
        inn = counterparty_data.get('inn')
        kpp = counterparty_data.get('kpp')
        counterparty = Counterparty.objects.get(inn=inn, kpp=kpp)

        if counterparty:
            return counterparty
        else:
            return Counterparty.objects.create(
                inn = inn,
                kpp = kpp,
                default = {
                    'name': counterparty_data.get('name'),
                    'name_full': counterparty_data.get('name_full')})

    def _order_cargo_update_or_create(self, order: TransportOrder, cargo_data: list[dict]) -> list[TransportOrderCargo]:
        result = []
        TransportOrderCargo.objects.filter(order=order).delete()
        for item_data in cargo_data:
            result += TransportOrderCargo.objects.create(
                order = order,
                default = {
                    'name': item_data.get('name'),
                    'hazard_class': item_data.get('hazard_class', ''),
                    'weight': item_data.get('weight', 0.0),
                    'weight_unit': item_data.get('weight_unit', ''),
                    'volume': item_data.get('volume', 0.0),
                    'volume_unit': item_data.get('volume_unit', ''),
                    'comment': item_data.get('comment', '')})
        return result

    def _order_truck_requirements_update_or_create(self, order: TransportOrder, truck_requirements_data: dict) -> TransportOrderTruckReqts:
        TransportOrderTruckReqts.objects.filter(order=order).delete()
        return TransportOrderTruckReqts.objects.create(
            order = order,
            default = {
                'weight': truck_requirements_data.get('weight', 0.0),
                'weight_unit': truck_requirements_data.get('weight_unit', ''),
                'volume': truck_requirements_data.get('volume', 0.0),
                'volume_unit': truck_requirements_data.get('volume_unit', ''),
                'refrigeration': truck_requirements_data.get('refrigeration'),
                'temperature': truck_requirements_data.get('volume_unit', 0),
                'comment': truck_requirements_data.get('comment', '')})

    def _order_routepoints_update_or_create(self, order: TransportOrder, routepoints_data: list[dict]) -> list[TransportOrderRoutepoint]:
        result = []
        TransportOrderRoutepoint.objects.filter(order=order).delete()
        for item_data in routepoints_data:
            result += TransportOrderRoutepoint.objects.create(
                order = order,
                default = {
                    'action': EnumTransportOrderStatus.objects.get(code_str=item_data.get('action')),
                    'date_start': item_data.get('date_start'),
                    'date_end': item_data.get('date_end'),
                    'address': item_data.get('address'),
                    'counterparty': item_data.get('counterparty', ''),
                    'contact_person': item_data.get('contact_person', ''),
                    'comment': item_data.get('comment', '')})
        return result
