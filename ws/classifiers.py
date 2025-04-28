
import json
import requests
from django.conf import settings
from typing import Any, Dict, Tuple


class WSClassifiers:
    class URNs:
        currency = '/api/v1/currency'
        unit = '/api/v1/unit'
        units = '/api/v1/units'
        rate_vat = '/api/v1/rate_vat'
        cargo_hazard = '/api/v1/cargo_hazard'

    def __init__(self):
        self.url = settings.WEB_SERVICES.get('classifiers').get('URL')
        self.base_headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'User-Agent': 'Django Client'
        }

    def get_currency(self, params: Dict = None) -> Tuple[Any, bool]:
        return self._request(requests.get, self.URNs.currency, params)

    def get_unit_by_code_str(self, code_str: str) -> Tuple[Any, bool]:
        return self._request(requests.get, self.URNs.unit, {'code_str': code_str})

    def get_units(self, params: Dict = None) -> Tuple[Any, bool]:
        return self._request(requests.get, self.URNs.units, params)

    def get_rate_vat(self, params: Dict = None) -> Tuple[Any, bool]:
        return self._request(requests.get, self.URNs.rate_vat, params)

    def get_cargo_hazard(self, params: Dict = None) -> Tuple[Any, bool]:
        return self._request(requests.get, self.URNs.cargo_hazard, params)

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