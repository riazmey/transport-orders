
from typing import Tuple
from django.db import transaction

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

from subscriptions.models import(
    Subscription,
    SubscriptionOrder)


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
            pks = []
            for order_data in data:
                order_current = self._order_update_or_create(order_data)
                pks.append(order_current.pk)
                result.append(order_current)
            if pks:
                result += self._orders_set_status_excluded(pks)
        return result, success

    def orders_mixin_get(self) -> Tuple[list[dict], bool]:
        return [], False

    def _orders_set_status_excluded(self, pks: list) -> list[TransportOrder]:
        result = []
        status_closed = EnumTransportOrderStatus.objects.get(code_str='closed')
        orders_excluded = TransportOrder.objects.exclude(status__pk=status_closed.pk).exclude(pk__in=pks)
        for order in orders_excluded:
            TransportOrder.objects.filter(pk=order.pk).update(status = status_closed)
            self._add_order_to_subscriptions(order)
        return result

    def _order_update_or_create(self, order_data: dict) -> TransportOrder:
        order_changed = False
        counterparty = self._counterparty_update_or_create(order_data.get('counterparty'))
        modified = order_data.get('modified')
        status = EnumTransportOrderStatus.objects.get(code_str=order_data.get('status'))
        currency = order_data.get('currency')
        price = order_data.get('price', 0.00)
        rate_vat = order_data.get('rate_vat')
        order = self._order_find(order_data)
        if order:
            if (not order.modified == modified or
                not order.status == status or
                not order.currency == currency or
                not order.price == price or
                not order.rate_vat == rate_vat):
                order_changed = True
                TransportOrder.objects.filter(pk=order.pk).update(
                    counterparty = counterparty, modified = modified, status = status,
                    currency = currency, price = price, rate_vat = rate_vat)
        else:
            order_changed = True
            order = TransportOrder.objects.create(market = self.market,
                counterparty = counterparty, modified = modified,
                status = status, currency = currency, price = price,
                rate_vat = rate_vat)
        
        self._order_external_id_create(order, order_changed, order_data.get('external_id'))
        self._order_cargo_update_or_create(order, order_changed, order_data.get('cargo'))
        self._order_truck_requirements_update_or_create(order, order_changed, order_data.get('truck_requirements'))
        self._order_routepoints_update_or_create(order, order_changed, order_data.get('routepoints'))

        if order_changed:
            self._add_order_to_subscriptions(order)

        return order

    def _counterparty_update_or_create(self, counterparty_data: dict) -> Counterparty:
        inn = counterparty_data.get('inn')
        kpp = counterparty_data.get('kpp')
        counterparty_params = {'inn': inn, 'kpp': kpp}

        if Counterparty.objects.filter(**counterparty_params).exists():
            return Counterparty.objects.get(**counterparty_params)
        else:
            return Counterparty.objects.create(inn = inn, kpp = kpp,
                name = counterparty_data.get('name'),
                name_full = counterparty_data.get('name_full'))

    def _order_find(self, order_data: dict) -> TransportOrder | None:
        external_id = order_data.get('external_id')
        params_external_id = {
            'market': self.market,
            'external_id': external_id.get('external_id')}
        if TransportOrderExternalID.objects.filter(**params_external_id).exists():
            return TransportOrderExternalID.objects.get(**params_external_id).order
        else:
            return None

    def _order_external_id_create(self, order: TransportOrder,
                                  order_changed: bool, external_id_data: dict):
        external_id = external_id_data.get('external_id')
        external_code = external_id_data.get('external_code')
        if TransportOrderExternalID.objects.filter(market=self.market, order=order).exists():
            external_id_obj = TransportOrderExternalID.objects.get(market=self.market, order=order)
            if (not external_id_obj.external_id == external_id or
                not external_id_obj.external_code == external_code):
                order_changed = True
                TransportOrderExternalID.objects.filter(market=self.market, order=order).update(
                    external_id = external_id, external_code = external_code)
        else:
            order_changed = True
            TransportOrderExternalID.objects.create(market = self.market,
                order = order, external_id = external_id, external_code = external_code)

    def _order_cargo_update_or_create(self, order: TransportOrder,
                                      order_changed: bool, cargo_data: list[dict]):
        cargos_edited = False
        start_cargos = TransportOrderCargo.objects.filter(order=order)
        if len(start_cargos) != len(cargo_data):
            cargos_edited = True
        else:
            for i in range(len(start_cargos)):
                item_cargo_db = start_cargos[i]
                item_cargo_data = cargo_data[i]
                item_cargo_data_name = item_cargo_data.get('name', '')[0:150]
                item_cargo_data_hazard_class = item_cargo_data.get('hazard_class', '0')[0:5]
                item_cargo_data_weight = item_cargo_data.get('weight', 0.0)
                item_cargo_data_weight_unit = item_cargo_data.get('weight_unit', '')[0:4]
                item_cargo_data_volume = item_cargo_data.get('volume', 0.0)
                item_cargo_data_volume_unit = item_cargo_data.get('volume_unit', '')[0:4]
                if (not item_cargo_db.name == item_cargo_data_name or
                    not item_cargo_db.hazard_class == item_cargo_data_hazard_class or
                    not item_cargo_db.weight == item_cargo_data_weight or
                    not item_cargo_db.weight_unit == item_cargo_data_weight_unit or
                    not item_cargo_db.volume == item_cargo_data_volume or
                    not item_cargo_db.volume_unit == item_cargo_data_volume_unit):
                    cargos_edited = True
                    break
        if cargos_edited:
            order_changed = True
            TransportOrderCargo.objects.filter(order=order).delete()
            for item_data in cargo_data:
                TransportOrderCargo.objects.create(
                    order = order,
                    name = item_data.get('name', '')[0:150],
                    hazard_class = item_data.get('hazard_class', '0')[0:5],
                    weight = item_data.get('weight', 0.0),
                    weight_unit = item_data.get('weight_unit', '')[0:4],
                    volume = item_data.get('volume', 0.0),
                    volume_unit = item_data.get('volume_unit', '')[0:4])

    def _order_truck_requirements_update_or_create(self, order: TransportOrder,
                                                   order_changed: bool, truck_requirements_data: dict):
        weight = truck_requirements_data.get('weight', 0.00)
        weight_unit = truck_requirements_data.get('weight_unit', '')[0:4]
        volume = truck_requirements_data.get('volume', 0.00)
        volume_unit = truck_requirements_data.get('volume_unit', '')[0:4]
        refrigeration = truck_requirements_data.get('refrigeration')
        temperature = truck_requirements_data.get('temperature', 0)
        if TransportOrderTruckReqts.objects.filter(order=order).exists():
            truck_requirements = TransportOrderTruckReqts.objects.get(order=order)
            if (not truck_requirements.weight == weight or
                not truck_requirements.weight_unit == weight_unit or
                not truck_requirements.volume == volume or
                not truck_requirements.volume_unit == volume_unit or
                not truck_requirements.refrigeration == refrigeration or
                not truck_requirements.temperature == temperature):
                order_changed = True
                TransportOrderTruckReqts.objects.filter(order=order).update(
                    weight = weight, weight_unit = weight_unit, volume = volume,
                    volume_unit = volume_unit, refrigeration = refrigeration,
                    temperature = temperature)
        else:
            order_changed = True
            TransportOrderTruckReqts.objects.create(order = order,
                weight = weight, weight_unit = weight_unit, volume = volume,
                volume_unit = volume_unit, refrigeration = refrigeration,
                temperature = temperature)

    def _order_routepoints_update_or_create(self, order: TransportOrder,
                                            order_changed: bool, routepoints_data: list[dict]):
        routepoints_edited = True
        start_routepoints = TransportOrderRoutepoint.objects.filter(order=order)
        if len(start_routepoints) != len(routepoints_data):
            routepoints_edited = True
        else:
            for i in range(len(start_routepoints)):
                item_routepoint_db = start_routepoints[i]
                item_routepoint_data = routepoints_data[i]
                item_routepoint_address = item_routepoint_data.get('address', '')[0:1024]
                item_routepoint_action = EnumRoutepointAction.objects.get(code_str=item_routepoint_data.get('action'))
                item_routepoint_date_start = item_routepoint_data.get('date_start')
                item_routepoint_date_end = item_routepoint_data.get('date_end')
                item_routepoint_counterparty = item_routepoint_data.get('counterparty', '')[0:255]
                item_routepoint_contact_person = item_routepoint_data.get('contact_person', '')[0:255]
                if (not item_routepoint_db.address == item_routepoint_address or
                    not item_routepoint_db.action == item_routepoint_action or
                    not item_routepoint_db.date_start == item_routepoint_date_start or
                    not item_routepoint_db.date_end == item_routepoint_date_end or
                    not item_routepoint_db.counterparty == item_routepoint_counterparty or
                    not item_routepoint_db.contact_person == item_routepoint_contact_person):
                    routepoints_edited = True
                    break
        if routepoints_edited:
            order_changed = True
            TransportOrderRoutepoint.objects.filter(order=order).delete()
            for item_data in routepoints_data:
                TransportOrderRoutepoint.objects.create(
                    order = order,
                    address = item_data.get('address')[0:1024],
                    action = EnumRoutepointAction.objects.get(code_str=item_data.get('action')),
                    date_start = item_data.get('date_start'),
                    date_end = item_data.get('date_end'),
                    counterparty = item_data.get('counterparty', '')[0:255],
                    contact_person = item_data.get('contact_person', '')[0:255])

    def _add_order_to_subscriptions(self, order: TransportOrder):
        subscriptions = Subscription.objects.filter(model='TransportOrder')
        if subscriptions:
            for subscription in subscriptions:
                if not SubscriptionOrder.objects.filter(subscription=subscription, order=order).exists():
                    SubscriptionOrder.objects.create(
                        subscription = subscription,
                        order = order)
