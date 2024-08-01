import logging
from core.garobot import Garobot
from core.shop import Shop
from core.scheduler import Scheduler
from api.api import API

def init_logger() -> None:
    logging.basicConfig(level=logging.INFO,
                        format='{asctime} :: {levelname} :: {module} :: {funcName} :: {message}',
                        style='{',
                        handlers=[
                            logging.StreamHandler()
                        ])
    
def handle_service_employee_input(shop: Shop) -> tuple[int, int]:
    services = sorted(shop.get_services(), key=lambda x: x.service_name)
    for service in services:
        print('Service ID: {}\nService name: {}\nService price: {}\n'.format(service.get_service_id(),
                                                                             service.get_service_name(),
                                                                             service.get_service_price()
                                                                             ))
    print('Enter service id: ')
    service_id = int(input().strip())

    employees = sorted(shop.get_employees(), key=lambda x: x.employee_name)
    for employee in employees:
        print('Employee ID: {}\nEmployee name: {}\n'.format(employee.get_employee_id(),
                                                            employee.get_employee_name()
                                                            ))
    print('Enter employee id: ')
    employee_id = int(input().strip())
    return service_id, employee_id

def main() -> None:
    init_logger()

    api = API()
    api.regiser_endpoints()
    print('Enter business name: ')
    business_name = input().strip()
    business_id = api.get_business_id(business_name)

    shop = Shop(business_id)
    garobot = Garobot(shop, api)
    garobot.populate_shop()
    service_id, employee_id = handle_service_employee_input(shop)

    selected_service = shop.get_service_by_id(service_id)
    selected_employee = shop.get_employee_by_id(employee_id)
    if selected_service is not None and selected_employee is not None:
        garobot.set_service(selected_service)
        garobot.set_employee(selected_employee)
        Scheduler(garobot)
    else:
        logging.error('Unable to find service or employee!')
        raise SystemExit()

if __name__ == '__main__':
    main()