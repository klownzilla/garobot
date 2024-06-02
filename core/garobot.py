import logging, requests.exceptions, random
from typing import Any
from datetime import datetime
import api.api as garobot_api
import api.api_data as api_data
import core.shop as garobot_shop
from core.constants import ENDPOINTS

class Garobot:
    def __init__(self, shop: garobot_shop.Shop, api: garobot_api.API, business_id: int) -> None:
        self.logger = logging.getLogger(__name__)
        self.shop = shop
        self.api = api
        self.business_id = business_id
        self._register_endpoints()
    
    def _get_shop(self) -> garobot_shop.Shop:
        return self.shop
    
    def _get_api(self) -> garobot_api.API:
        return self.api
    
    def _get_business_id(self) -> int:
        return self.business_id
    
    def _get_service(self) -> garobot_shop.Service:
        return self.service
    
    def set_service(self, service: garobot_shop.Service) -> None:
        self.service = service
    
    def _get_employee(self) -> garobot_shop.Employee:
        return self.employee
    
    def set_employee(self, employee: garobot_shop.Employee) -> None:
        self.employee = employee
    
    def _register_endpoints(self) -> None:
        for endpoint_identifier, endpoint_value in ENDPOINTS.items():
            self.logger.debug('{},{}'.format(endpoint_identifier, endpoint_value))
            endpoint = garobot_api.Endpoint(endpoint_identifier, endpoint_value)
            self._get_api().add_endpoint(endpoint)

    def _populate_shop_api_call(self) -> tuple[dict[Any, str], dict[Any, str]]:
        try:
            self.logger.info('Trying API call...')
            req = self._get_api().make_post_request('get_bookings',
                                                    api_data.get_shop_booking_data(
                                                        self._get_business_id()
                                                    ))
        except requests.exceptions.RequestException as e:
            self.logger.error(e)
            raise SystemExit(e)
        try:
            shop_service_list = req.json().get('lstOnlineServiceDetail')
            shop_employee_list = req.json().get('lstOnlineServiceProviderDetail')
        except ValueError as e:
            self.logger.error(e)
            raise SystemExit(e)
        self.logger.info('API call success!')
        return shop_service_list, shop_employee_list

    def populate_shop(self) -> None:
        self.logger.info('Start populating shop!')
        shop_service_list, shop_employee_list = self._populate_shop_api_call()
        for shop_service in shop_service_list:
            service = garobot_shop.Service(shop_service['serviceID'],
                                            shop_service['serviceTitle'],
                                            shop_service['price'],
                                            shop_service['serviceDesc']
                                            )
            self._get_shop().add_service(service)
        
        for shop_employee in shop_employee_list:
            employee = garobot_shop.Employee(shop_employee['id'],
                                              shop_employee['text']
                                              )
            self._get_shop().add_employee(employee)
        self.logger.info('Done populating shop!')

    def _populate_appointments_api_call(self) -> tuple[str, str]:
        try:
            self.logger.info('Trying API call...')
            req = self._get_api().make_post_request('get_appointments',
                                                    api_data.get_shop_appointment_data(
                                                        self._get_business_id(),
                                                        self._get_service().get_service_id(),
                                                        self._get_employee().get_employee_id()
                                                    ))
        except requests.exceptions.RequestException as e:
            self.logger.error(e)
            raise SystemExit(e)
        
        try:
            available_date = req.json().get('d')[0]['AppDate']
            available_times = req.json().get('d')[0]['AvailableTime']
        except ValueError as e:
            self.logger.error(e)
            raise SystemExit(e)
        self.logger.info('API call success!')
        return available_date, available_times

    def populate_appointments(self) -> None:
        self.logger.info('Start populating appointments!')
        available_date, available_times = self._populate_appointments_api_call()

        appointments_before = self._get_shop().get_appointments().copy()
        if ',' in available_times:
            available_times = available_times.split(',')
            
        for time in available_times:
            available_date_time = available_date + " " + time
            appointment_date_time = datetime.strptime(available_date_time, '%d %b %Y %H:%M %p')
            appointment = garobot_shop.Appointment(random.randint(0, 5000), appointment_date_time, self._get_service(), self._get_employee())
            if appointment.get_appointment_date_time() == self._get_shop().get_appointment_by_date_time(appointment_date_time).get_appointment_date_time():
                self.logger.info('Found existing appointment! Skipping...')
            else:
                self._get_shop().add_appointment(appointment)
        appointments_after = self._get_shop().get_appointments()

        if len(appointments_before) < len(appointments_after):
            self.logger.info('Found new appointment!')
            for new_appointment in appointments_after:
                if new_appointment not in appointments_before:
                    self.logger.info(new_appointment)
        elif len(appointments_before) > len(appointments_after):
            self.logger.info('Lost appointment!')
            for old_appointment in appointments_before:
                if old_appointment not in appointments_after:
                    self.logger.info(old_appointment)
        else:
            self.logger.info('No new appointments...')
        self.logger.info('Done populating appointments!')

    def determine_best_appointment(self) -> garobot_shop.Appointment:
        self.logger.info('Determining best appointment...')
        appointments = self._get_shop().get_appointments()
        best_appointment = appointments[0]
        for appointment in appointments:
            if appointment.get_appointment_date_time() < best_appointment.get_appointment_date_time():
                best_appointment = appointment
        for appointment in appointments:
            self.logger.info(appointment)
        return best_appointment