
import json
import requests
from django.conf import settings
from typing import Any, Dict, Tuple
from ws.classifiers import WSClassifiers

class WSMarketplaceAtrucks:

    class URNs:
        order = '/api/v3/carrier/orders/'
        auction = '/api/v3/customer/auctions/'

    def order_get(self) -> (list[dict] | bool):
        data, success = self.get_list_goods()
        return [], False
    
    def _request(self, method: requests.Request, urn: str, params: Dict = None) -> Tuple[Any, bool]:
        url = f'{self.url}{urn}'
        headers = self.base_headers.copy()
        
        try:
            response = method(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            return data, True
        
        except requests.RequestException as e:
            return str(e), False
        except json.JSONDecodeError as e:
            return f"Error parsing JSON: {e}", False