
import json
import requests
from django.conf import settings
from typing import Any, Dict, Tuple, List


class WSClassifiers:
    class URNs:
        currencies = '/api/v1/currencies'
        currency = '/api/v1/currency'
        unit = '/api/v1/unit'
        units = '/api/v1/units'
        rate_vat = '/api/v1/rate_vat'
        rates_vat = '/api/v1/rates_vat'
        cargo_hazard = '/api/v1/cargo_hazard'
        cargos_hazards = '/api/v1/cargos_hazards'

    def __init__(self):
        self.url = settings.WEB_SERVICES.get('classifiers').get('URL')
        self.base_headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'User-Agent': 'Django Client'}

    def list_currencies(self) -> List[Tuple[str, str]]:
        result = []
        currencies, success = self.get_currencies()
        if success:
            for currency_data in currencies:
                code_str = currency_data.get('code_str')
                name = currency_data.get('name')
                result.append((code_str, name))
        return result

    def list_units(self, params: Dict) -> List[Tuple[str, str]]:
        result = []
        units, success = self.get_units(params)
        if success:
            for unit_data in units:
                code_dec = unit_data.get('code_dec')
                name = unit_data.get('name')
                result.append((code_dec, name))
        return result
    
    def list_cargos_hazards(self) -> List[Tuple[str, str]]:
        result = []
        hazard_classes, success = self.get_cargos_hazards()
        if success:
            for class_data in hazard_classes:
                code_str = class_data.get('code_str')
                name = class_data.get('name')
                result.append((code_str, name))
        return result

    def list_rates_vat(self) -> List[Tuple[str, str]]:
        result = []
        rates_vat, success = self.get_rates_vat()
        if success:
            for vat_data in rates_vat:
                code_str = vat_data.get('code_str')
                repr = vat_data.get('repr')
                result.append((code_str, repr))
        return result

    def get_currency(self, params: Dict) -> Tuple[Any, bool]:
        return self._request(requests.get, self.URNs.currency, params)
    
    def get_currencies(self) -> Tuple[Any, bool]:
        return self._request(requests.get, self.URNs.currencies)

    def get_unit(self, code_dec: str) -> Tuple[Any, bool]:
        return self._request(requests.get, self.URNs.unit, {'code_dec': code_dec})

    def get_units(self, params: Dict) -> Tuple[Any, bool]:
        return self._request(requests.get, self.URNs.units, params)

    def get_rate_vat(self, params: Dict = None) -> Tuple[Any, bool]:
        return self._request(requests.get, self.URNs.rate_vat, params)

    def get_cargo_hazard(self, params: Dict = None) -> Tuple[Any, bool]:
        return self._request(requests.get, self.URNs.cargo_hazard, params)
    
    def get_cargos_hazards(self) -> Tuple[Any, bool]:
        return self._request(requests.get, self.URNs.cargos_hazards)

    def get_cargos_hazards(self) -> Tuple[Any, bool]:
        return self._request(requests.get, self.URNs.cargos_hazards)

    def get_rates_vat(self) -> Tuple[Any, bool]:
        return self._request(requests.get, self.URNs.rates_vat)

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
