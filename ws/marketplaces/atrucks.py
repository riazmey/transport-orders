
import json
import requests
from datetime import datetime
from dateutil import parser
from dateutil import tz
from typing import Any, Dict, Tuple
from django.core.exceptions import RequestAborted

import logging
logger = logging.getLogger(__name__)

class WSMarketplaceAtrucks:

    class URNs:
        order = '/api/v3/carrier/orders/'
        auction = '/api/v3/customer/auctions/'

    def __init__(self, market):
        super().__init__(market)
        self.base_headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Auth-Key': self.token}

    def orders_mixin_get(self) -> Tuple[list[dict], bool]:
        result = []
        data = []
        data_available, received = self._request(method=requests.get,
            urn=self.URNs.order, data='{"type": "available"}')
        if received:
            data += data_available
        data_obtained, received = self._request(method=requests.get,
            urn=self.URNs.order, data='{"type": "obtained"}')
        if received:
            data += data_obtained
        if received:
            for item_data in data:
                data_order = item_data.get('order')
                data_auction = item_data.get('auction_status')
                result.append(self._convert_data_ws_order(data_order, data_auction))
        return result, received
   
    def _request(self, method: requests.Request, urn: str, params: Dict = None, data: str = None) -> Tuple[Any, bool]:
        url = f'{self.url}{urn}'
        headers = self.base_headers.copy()
        
        try:
            response = method(url, headers=headers, params=params, data=data)
            response.raise_for_status()
            
            data_recieved = response.json()
            return data_recieved, True
        
        except requests.RequestException as e:
            message = f'API request failed: {str(e)}'
            logger.error(message)
            return message, False
        except json.JSONDecodeError as e:
            message = f'Error parsing JSON: {str(e)}'
            logger.error(message)
            return message, False

    @classmethod
    def _convert_data_ws_order(cls, data_order: dict, data_auction: dict = None) -> dict:
        return {
            'external_id': cls._convert_data_ws_order_external_id(data_order),
            'modified': cls._convert_data_ws_order_modified(data_order),
            'status': cls._convert_data_ws_order_status_code(data_order),
            'counterparty': cls._convert_data_ws_order_counterparty(data_order),
            'cargo': cls._convert_data_ws_order_cargo(data_order),
            'truck_requirements': cls._convert_data_ws_order_truck_requirements(data_order),
            'routepoints': cls._convert_data_ws_order_routepoints(data_order),
            'currency': data_order.get('currency'),
            'price': cls._convert_data_ws_order_price(data_order, data_auction),
            'rate_vat': cls._convert_data_ws_order_rate_vat(data_order)}

    @classmethod
    def _convert_data_ws_order_external_id(cls, data_order: dict) -> dict:
        order_id = data_order.get('order_id', '')[0:40]
        order_human_name = data_order.get('order_human_name', '')[0:40]
        if order_id:
            return {
                'external_id': order_id,
                'external_code': order_human_name}
        else:
            message = f'_convert_data_ws_order_external_id(data_order={data_order}):' + \
                ' The received data is missing the "order_id" property'
            logger.error(message)
            raise RequestAborted(message)

    @classmethod
    def _convert_data_ws_order_status_code(cls, data_order: dict) -> str:
        status = data_order.get('status', '')[0:50]
        status_code = cls._convert_data_ws_status_code(status)
        if status_code:
            return status_code
        else:
            message = f'_convert_data_ws_order_status_code(data_order={data_order}):' + \
                f'It was not possible to compare the received order status "{status}"'
            logger.error(message)
            raise RequestAborted(message)

    @classmethod
    def _convert_data_ws_order_modified(cls, data_order: dict) -> datetime:
        modification_timestamp = data_order.get('modification_timestamp', 0)
        if modification_timestamp:
            return datetime.fromtimestamp(modification_timestamp).astimezone(tz.tzutc())
        else:
            message = f'_convert_data_ws_order_modified(data_order={data_order}):' + \
                'The received data is missing the "modification_timestamp" property'
            logger.error(message)
            raise RequestAborted(message)

    @classmethod
    def _convert_data_ws_order_counterparty(cls, data_order: dict) -> dict:
        customer_company = data_order.get('customer_company')
        if isinstance(customer_company, dict) | len(customer_company) >= 4:
            return {
                'inn': cls._value_to_str(customer_company.get('inn'))[0:12],
                'kpp': cls._value_to_str(customer_company.get('kpp'))[0:9],
                'name': cls._value_to_str(customer_company.get('name', ''))[0:255],
                'name_full': cls._value_to_str(customer_company.get('requisite_name', ''))[0:255]}
        else:
            message = f'_convert_data_ws_order_counterparty(data_order={data_order}):' + \
                'The "customer_company" property is missing or incorrectly filled in the received data'
            logger.error(message)
            raise RequestAborted(message)


    @classmethod
    def _convert_data_ws_order_cargo(cls, data_order: dict) -> list[dict]:
        result = []
        cargo = data_order.get('cargo')
        if isinstance(cargo, dict) | len(cargo) >= 3:
            result.append({
                'name': cargo.get('name', '')[0:150],
                'hazard_class': cls._value_to_str(cargo.get('hazard_class', '0'))[0:5],
                'weight': cls._value_to_float(cargo.get('weight')),
                'weight_unit': '168',
                'volume': cls._value_to_float(cargo.get('volume')),
                'volume_unit': '113'})
        else:
            message = f'_convert_data_ws_order_cargo(data_order={data_order}):' + \
                'The "cargo" property is missing or incorrectly filled in the received data'
            logger.error(message)
            raise RequestAborted(message)
        return result

    @classmethod
    def _convert_data_ws_order_truck_requirements(cls, data_order: dict) -> dict:
        cargo = data_order.get('cargo')
        refrigeration = False
        temperature = 0
        temperature_conditions = cargo.get('temperature_conditions')
        if temperature_conditions:
            refrigeration = True
            temperature = cls._value_to_float(temperature_conditions)
        
        truck = data_order.get('truck')
        if isinstance(truck, dict) | len(truck) > 3:
            truck_types = truck.get('truck_types')
            if isinstance(truck_types, list) and truck_types.count('Рефрижератор'):
                refrigeration = True
            return {
                'weight': cls._value_to_float(truck.get('carrying_capacity')),
                'weight_unit': '168',
                'volume': cls._value_to_float(truck.get('carrying_volume')),
                'volume_unit': '113',
                'refrigeration': refrigeration,
                'temperature': temperature,
                'comment': cls._value_to_str(truck.get('carrying_description', ''))[0:1024]}
        else:
            message = f'_convert_data_ws_order_truck_requirements(data_order={data_order}):' + \
                'The "truck" property is missing or incorrectly filled in the received data'
            logger.error(message)
            raise RequestAborted(message)

    @classmethod
    def _convert_data_ws_order_routepoints(cls, data_order: dict) -> list[dict]:
        route = data_order.get('route')
        result = []
        if isinstance(route, dict):
            waypoints = route.get('waypoints')
            if isinstance(waypoints, list):
                for data_waypoint in waypoints:
                    arrival_date = data_waypoint.get('arrival_date')
                    address = data_waypoint.get('address')
                    result.append({
                        'action': cls._convert_data_ws_action(data_waypoint.get('waypoint_type')[0:50]),
                        'date_start': cls._value_to_date(arrival_date[0]),
                        'date_end': cls._value_to_date(arrival_date[1]),
                        'address': address.get('free_form', '')[0:1024],
                        'counterparty': cls._value_to_str(data_waypoint.get('counteragent', ''))[0:255],
                        'contact_person': cls._value_to_str(data_waypoint.get('contact_person', ''))[0:255],
                        'comment': cls._value_to_str(data_waypoint.get('comment', ''))[0:1024]})
            else:
                message = f'_convert_data_ws_order_routepoints(data_order={data_order}):' + \
                    'The "route.waypoints" propertys is missing or incorrectly filled in the received data'
                logger.error(message)
                raise RequestAborted(message)

        else:
            message = f'_convert_data_ws_order_routepoints(data_order={data_order}):' + \
                'The "route" property is missing in the received data'
            logger.error(message)
            raise RequestAborted(message)
        return result

    @classmethod
    def _convert_data_ws_order_price(cls, data_order: dict, data_auction: dict = None) -> float:
        price = cls._value_to_float(data_order.get('price', ''))
        start_price = cls._value_to_float(data_order.get('start_price', ''))
        current_price = None
        if data_auction:
            current_price = cls._value_to_float(data_auction.get('current_price', ''))
        
        if current_price:
            return current_price
        elif price:
            return price
        elif start_price:
            return start_price
        else:
            return 0.0

    @classmethod
    def _convert_data_ws_order_rate_vat(cls, data_order: dict) -> str:
        vat_type = ''
        start_price_vat_type = cls._value_to_str(data_order.get('start_price_vat_type'))
        current_price_vat_type = cls._value_to_str(data_order.get('current_price_vat_type'))
        if current_price_vat_type:
            vat_type = current_price_vat_type
        elif start_price_vat_type:
            vat_type = start_price_vat_type
        rate_vat = cls._convert_data_ws_rate_vat(vat_type)
        if rate_vat:
            return rate_vat
        else:
            message = f'_convert_data_ws_order_rate_vat(data_order={data_order}):' + \
                'The "start_price_vat_type, current_price_vat_type" propertys is missing or ' + \
                'incorrectly filled in the received data'
            logger.error(message)
            raise RequestAborted(message)

    @classmethod
    def _value_to_float(cls, value: any) -> float:
        result = 0.00
        if isinstance(value, float):
            result = value
        elif isinstance(value, int):
            result = float(value)
        elif isinstance(value, str) and value.replace('.','', 1).isdigit():
            result = float(value)
        return result

    @classmethod
    def _value_to_str(cls, value: any) -> float:
        result = ''
        if isinstance(value, str):
            result = value
        elif isinstance(value, int):
            result = str(value)
        elif isinstance(value, float):
            result = str(value)
        return result

    @classmethod
    def _value_to_date(cls, value: any) -> datetime | None:
        result = None
        if isinstance(value, str):
            result = parser.parse(value)
        elif isinstance(value, datetime):
            result = value
        return result

    @classmethod
    def _convert_data_ws_status_code(cls, value: str) -> str:
        result = ''
        match value:
            case 'deferred':
                result = 'draft'
            case 'auction':
                result = 'auction'
            case 'bundle_auction':
                result = 'auction'
            case 'in_bundle_auction':
                result = 'auction'
            case 'no_data':
                result = 'waiting_start'
            case 'in_bundle_no_data':
                result = 'waiting_start'
            case 'bundle_assigned':
                result = 'waiting_start'
            case 'in_progress':
                result = 'in_progress'
            case 'in_bundle_in_progress':
                result = 'in_progress'
            case 'completed':
                result = 'completed'
            case 'in_bundle_completed':
                result = 'completed'
        return result
    
    @classmethod
    def _convert_data_ws_action(cls, value: str) -> str:
        result = ''
        match value:
            case 'load':
                result = 'loading'
            case 'unload':
                result = 'unloading'
            case 'check':
                result = 'check'
        return result

    @classmethod
    def _convert_data_ws_rate_vat(cls, value: str) -> str:
        result = ''
        match value:
            case 'zero_vat':
                result = 'with_vat0'
            case 'with_vat':
                result = 'with_vat20'
            case 'with_vat5':
                result = 'with_vat5'
            case 'with_vat7':
                result = 'with_vat7'
            case 'without_vat':
                result = 'without_vat'
        return result
