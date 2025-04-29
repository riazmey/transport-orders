
import json
import requests
from datetime import datetime
from typing import Any, Dict, Tuple
from django.core.exceptions import RequestAborted
from orders.models import EnumTransportOrderStatus


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
            'counterparty',
            'cargo',
            'routepoints',
            'truck_requirements',
            'currency',
            'price',
            'rate_vat',
            'comment',
            'repr'
        )

    def convert_data_ws_order(self, data_order: dict) -> dict:

        order_status = data_order.get('order_status', '')
        status_code = self.convert_data_ws_status_code(order_status)
        if status_code:
            status = EnumTransportOrderStatus.objects.get(code_str=status_code)
        else:
            message = f'It was not possible to compare the received order status "{order_status}"'
            raise RequestAborted(message)

        modification_timestamp = data_order.get('modification_timestamp', 0)
        if modification_timestamp:
            created = datetime.fromtimestamp(modification_timestamp)
        else:
            message = 'The received data is missing the "modification_timestamp" property'
            raise RequestAborted(message)

        customer_company = data_order.get('customer_company', '')
        if customer_company:
            created = datetime.fromtimestamp(modification_timestamp)
        else:
            message = 'The received data is missing the "customer_company" property'
            raise RequestAborted(message)

        return {
            'market': self.market,
            'status': status,
            'created': created,
            'counterparty': counterparty,
            'market': self.market,
            'market': self.market,
            'market': self.market,
            'market': self.market,
            'market': self.market,
            'market': self.market,
            'market': self.market,
            'market': self.market,
            'market': self.market,
            'market': self.market,
            'market': self.market,
            'market': self.market,
            'market': self.market,
            'market': self.market,
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