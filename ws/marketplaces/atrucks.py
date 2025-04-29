
import json
import requests
from datetime import datetime
from typing import Any, Dict, Tuple
from django.core.exceptions import RequestAborted


class WSMarketplaceAtrucks:

    class URNs:
        order = '/api/v3/carrier/orders/'
        auction = '/api/v3/customer/auctions/'

    def __init__(self, market):
        super().__init__(market)
        self.base_headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Auth-Key': self.token
        }

    def orders_get(self) -> Tuple[list[dict], bool]:
        result_data = []
        data, received = self._request(requests.get, self.URNs.order)
        if received:
            for data_order in data:
                result_data.append(self.convert_data_ws_order(data_order))
        return result_data, received
    
        fields = (
            'routepoints',
            'currency',
            'price',
            'rate_vat',
            'comment',
            'repr'
        )

    def convert_data_ws_order(self, data_order: dict) -> dict:

        order_status = data_order.get('order_status', '')
        status_code = self.convert_data_ws_status_code(order_status)
        if not status_code:
            message = f'It was not possible to compare the received order status "{order_status}"'
            raise RequestAborted(message)

        modification_timestamp = data_order.get('modification_timestamp', 0)
        if modification_timestamp:
            created = datetime.fromtimestamp(modification_timestamp)
        else:
            message = 'The received data is missing the "modification_timestamp" property'
            raise RequestAborted(message)

        customer_company = data_order.get('customer_company')
        if isinstance(customer_company, dict) | len(customer_company) >= 4:
            counterparty = {
                'inn': customer_company.get('inn', ''),
                'kpp': customer_company.get('kpp', ''),
                'name': customer_company.get('name', ''),
                'name_full': customer_company.get('requisite_name', '')
            }
        else:
            message = 'The "customer_company" property is missing or incorrectly filled in the received data'
            raise RequestAborted(message)

        refrigeration = False
        temperature = 0
        cargo = data_order.get('cargo')
        if isinstance(cargo, dict) | len(cargo) >= 3:
            temperature_conditions = customer_company.get('temperature_conditions')
            if temperature_conditions:
                refrigeration = True
                temperature = self.value_to_float(temperature_conditions)
            cargo = {
                'name': customer_company.get('name', ''),
                'weight': self.value_to_float(customer_company.get('weight')),
                'weight_unit': '168',
                'volume': self.value_to_float(customer_company.get('volume')),
                'volume_unit': '113',
            }
        else:
            message = 'The "cargo" property is missing or incorrectly filled in the received data'
            raise RequestAborted(message)

        truck = data_order.get('truck')
        if isinstance(truck, dict) | len(truck) > 3:
            truck_types = truck.get('truck_types')
            if isinstance(truck_types, list) and truck_types.count('Рефрижератор'):
                refrigeration = True
            truck_requirements = {
                'weight': self.value_to_float(truck.get('carrying_capacity')),
                'weight_unit': '168',
                'volume': self.value_to_float(truck.get('carrying_volume')),
                'volume_unit': '113',
                'refrigeration': refrigeration,
                'temperature': temperature,
                'comment': truck.get('carrying_description', ''),
            }
        else:
            message = 'The "truck" property is missing or incorrectly filled in the received data'
            raise RequestAborted(message)

        route = data_order.get('route')
        routepoints = []
        if isinstance(route, dict):
            waypoints = data_order.get('waypoints')
            if isinstance(waypoints, list):

                for data_waypoint in waypoints:
                    routepoints.append(
                        {
                            'action': self.convert_data_ws_action(data_waypoint.get('waypoint_type')),
                            'date': self.convert_data_ws_action(data_waypoint.get('waypoint_type')),
                        }
                    )

                truck_types = truck.get('truck_types')
                if isinstance(truck_types, list) and truck_types.count('Рефрижератор'):
                    refrigeration = True
                truck_requirements = {
                    'weight': self.value_to_float(truck.get('carrying_capacity')),
                    'weight_unit': '168',
                    'volume': self.value_to_float(truck.get('carrying_volume')),
                    'volume_unit': '113',
                    'refrigeration': refrigeration,
                    'temperature': temperature,
                    'comment': truck.get('carrying_description', ''),
                }
            else:
                message = 'The "truck" property is missing or incorrectly filled in the received data'
                raise RequestAborted(message)

        else:
            message = 'The "route" property is missing in the received data'
            raise RequestAborted(message)

        return {
            'status': status_code,
            'created': created,
            'counterparty': counterparty,
            'cargo': cargo,
            'truck_requirements': truck_requirements,
            'routepoints': routepoints,
        }

    def convert_data_ws_status_code(self, value: str) -> str:
        result = ''
        match value:
            case 'deferred':
                result = 'draft'
            case 'auction':
                result = 'auction'
            case 'no_data':
                result = 'waiting_start'
            case 'in_progress':
                result = 'in_progress'
            case 'completed':
                result = 'completed'
        return result
    
    def convert_data_ws_action(self, value: str) -> str:
        result = ''
        match value:
            case 'load':
                result = 'loading'
            case 'unload':
                result = 'unloading'
        return result
   
    def _request(self, method: requests.Request, urn: str, params: Dict = None) -> Tuple[Any, bool]:
        url = f'{self.url}{urn}'
        headers = self.base_headers.copy()
        
        try:
            print(f'url: {url}')
            response = method(url, headers=headers, params=params)
            print(f'response: {response}')
            response.raise_for_status()
            
            data = response.json()
            print(f'data: {data}')
            return data, True
        
        except requests.RequestException as e:
            return str(e), False
        except json.JSONDecodeError as e:
            return f"Error parsing JSON: {e}", False

    @staticmethod
    def value_to_float(value: any) -> float:
        result = 0.0
        if isinstance(value, float):
            result = value
        elif isinstance(value, int):
            result = float(value)
        elif isinstance(value, str) | value.replace('.','',1).isdigit():
            result = float(value)
        return result