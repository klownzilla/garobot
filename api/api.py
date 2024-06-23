from __future__ import annotations
import logging, requests, json
from api.constants import API_URL, HEADER, ENDPOINTS

class API:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self.endpoints = set()
        self._set_request_headers()

    def regiser_endpoints(self) -> None:
        self.logger.info('Start registering endpoints...')
        for endpoint_identifier, endpoint_value in ENDPOINTS.items():
            self.logger.debug('{},{}'.format(
                endpoint_identifier,
                endpoint_value
                ))
            endpoint = Endpoint(endpoint_identifier, endpoint_value)
            self._add_endpoint(endpoint)
        self.logger.info('Done registering endpoints!')

    def make_post_request(self, endpoint_identifier: str, post_data: dict[str, str]) -> requests.Response:
        endpoint = self._get_endpoint(endpoint_identifier)
        self.logger.debug('{},{}'.format(endpoint._get_full_url(),
                                         post_data
                                         ))
        request = self._get_session().post(endpoint._get_full_url(), json=post_data)
        return request
    
    def _get_session(self) -> requests.Session:
        return self.session
    
    def _set_request_headers(self) -> None:
        self._get_session().headers.update(HEADER)

    def close_session(self) -> None:
        self.logger.info('Closing session...')
        self._get_session().close()

    def _add_endpoint(self, endpoint: Endpoint) -> None:
        self._get_endpoints().add(endpoint)

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