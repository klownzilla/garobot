from __future__ import annotations
import logging, requests, json
from constants import API_URL, HEADER

class API:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.endpoints = set()

    def add_endpoint(self, endpoint: Endpoint) -> None:
        self._get_endpoints().add(endpoint)

    def make_post_request(self, endpoint_identifier: str, post_data: dict) -> requests.Response:
        endpoint = self._get_endpoint(endpoint_identifier)
        self.logger.debug('{},{},{}'.format(endpoint._get_full_url(), post_data, HEADER))
        request = requests.post(endpoint._get_full_url(), json=post_data, headers=HEADER)
        return request

    def _get_endpoint(self, endpoint_identifier: str) -> Endpoint:
        endpoints = self._get_endpoints()
        for endpoint in endpoints:
            if endpoint._get_identifier() == endpoint_identifier:
                return endpoint
        return Endpoint('', '')

    def _get_endpoints(self) -> set[Endpoint]:
        return self.endpoints
    
class Endpoint:
    def __init__(self, endpoint_identifier: str, endpoint_value: str) -> None:
        self.endpoint_identifier = endpoint_identifier
        self.endpoint_value = endpoint_value

    def _get_full_url(self) -> str:
        return API_URL + self._get_value()

    def _get_identifier(self) -> str:
        return self.endpoint_identifier
    
    def _get_value(self) -> str:
        return self.endpoint_value
    
    def __str__(self) -> str:
        obj_dict = {
            'identifier':self._get_identifier(),
            'value':self._get_value()
        }
        return json.dumps(obj_dict)
        