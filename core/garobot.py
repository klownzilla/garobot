import requests, logging
import api as garobot_api
import api_data
import shop as garobot_shop

logger = logging.getLogger(__name__)  

class Garobot:
    def __init__(self, Shop: garobot_shop.Shop, API: garobot_api.API, business_id: int) -> None:
        self.shop = Shop
        self.api = API
        self.business_id = business_id
        self.service_id = 0
        self.employee_id = 0
    
    def get_shop(self) -> garobot_shop.Shop:
        return self.shop
    
    def get_api(self) -> garobot_api.API:
        return self.api
    
    def get_business_id(self) -> int:
        return self.business_id
    
    def get_service_id(self) -> int:
        return self.service_id
    
    def set_service_id(self, service_id: int) -> None:
        self.service_id = service_id
    
    def get_employee_id(self) -> int:
        return self.employee_id
    
    def set_employee_id(self, employee_id: int) -> None:
        self.employee_id = employee_id
    
    def populate_endpoints(self) -> None:
        #TODO: read from a config file instead
        e0 = garobot_api.Endpoint('get_bookings', 'getonlinebookingtabdetail')
        e1 = garobot_api.Endpoint('get_appointments', 'getavailablemultiappointments')
        self.get_api().add_endpoint(e0)
        self.get_api().add_endpoint(e1)

    def populate_shop(self) -> None:
        try:
            req = self.get_api().make_post_request('get_bookings', api_data.get_shop_booking_data(self.get_business_id()))
        except requests.exceptions.RequestException as e:
            logger.error(e)
            raise SystemExit(e)
        req_json = req.json()
        shop_service_list = req_json.get('lstOnlineServiceDetail')
        shop_employee_list = req_json.get('lstOnlineServiceProviderDetail')
        for shop_service in shop_service_list:
            service = garobot_shop.Service(shop_service['serviceID'], 
                                            shop_service['serviceTitle'],
                                            shop_service['price'],
                                            shop_service['serviceDesc']
                                            )
            self.get_shop().add_service(service)
        
        for shop_employee in shop_employee_list:
            employee = garobot_shop.Employee(shop_employee['id'],
                                             shop_employee['text']
                                             )
            self.get_shop().add_employee(employee)

    def populate_appointments(self) -> None:
        try:
            req = self.get_api().make_post_request('get_appointments', api_data.get_shop_appointment_data(self.get_business_id(),
                                                                                                  self.get_service_id(),
                                                                                                  self.get_employee_id()
                                                                                                  ))
        except requests.exceptions.RequestException as e:
            logger.error(e)
            raise SystemExit(e)
        req_json = req.json()
        #TODO: complete
        logger.info(req_json)

def main():
    logging.basicConfig(level=logging.INFO,
                    format='{asctime} :: {levelname} :: {funcName} :: {message}',
                    style='{',
                    handlers=[
                        logging.StreamHandler()
                    ])

    #TODO: make ids input
    business_id = 170649
    garobot = Garobot(garobot_shop.Shop(), garobot_api.API(), business_id)
    garobot.populate_endpoints()
    garobot.populate_shop()
    #I select my employee and service
    service_id = 16663123
    employee_id = 44120875
    garobot.set_service_id(service_id)
    garobot.set_employee_id(employee_id)
    garobot.populate_appointments()

if __name__ == '__main__':
    main()