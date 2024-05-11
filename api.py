from __future__ import annotations
import requests, json, logging
from constants import API_URL, HEADER

logger = logging.getLogger(__name__)

class API:
    def __init__(self) -> None:
        self.endpoints = set()

    def add_endpoint(self, endpoint: Endpoint) -> None:
        self._get_endpoints().add(endpoint)

    def make_post_request(self, endpoint_identifier: str, post_data: dict) -> requests.Response:
        endpoint = self._get_endpoint(endpoint_identifier)
        logger.debug('{},{},{}'.format(endpoint.get_full_url(), post_data, HEADER))
        request = requests.post(endpoint.get_full_url(), json=post_data, headers=HEADER)
        return request

    def _get_endpoint(self, endpoint_identifier: str) -> Endpoint:
        endpoints = self._get_endpoints()
        for endpoint in endpoints:
            if endpoint.get_identifier() == endpoint_identifier:
                return endpoint
        return Endpoint('', '')

    def _get_endpoints(self) -> set:
        return self.endpoints
    
    
class Endpoint:
    def __init__(self, endpoint_identifier: str, endpoint_value: str) -> None:
        self.endpoint_identifier = endpoint_identifier
        self.endpoint_value = endpoint_value

    def get_full_url(self) -> str:
        return API_URL + self.get_value()

    def get_identifier(self) -> str:
        return self.endpoint_identifier
    
    def get_value(self) -> str:
        return self.endpoint_value
    
    def _str_(self) -> str:
        obj_dict = {
            'identifier':self.get_identifier(),
            'value':self.get_value()
        }
        return json.dumps(obj_dict)
        