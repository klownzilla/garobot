import logging
from core.garobot import Garobot
from core.shop import Shop
from core.scheduler import Scheduler
from api.api import API
from core.constants import FREQUENCY

def init_logger() -> None:
    logging.basicConfig(level=logging.INFO,
                        format='{asctime} :: {levelname} :: {module} :: {funcName} :: {message}',
                        style='{',
                        handlers=[
                            logging.StreamHandler()
                        ])

def main() -> None:
    init_logger()

    api = API()
    api.regiser_endpoints()
    #TODO: make ids input
    business_id = 170649
    shop = Shop(business_id)
    garobot = Garobot(shop, api)
    #ask shop here -> populate shop
    garobot.populate_shop()
    #show employees + services -> ask to enter -> set and populate appts
    service_id = 16663123
    employee_id = 44120875

    selected_service = shop.get_service_by_id(service_id)
    selected_employee = shop.get_employee_by_id(employee_id)
    if selected_service is not None and selected_employee is not None:
        garobot.set_service(selected_service)
        garobot.set_employee(selected_employee)
        Scheduler(garobot, FREQUENCY)
    else:
        logging.error('Unable to find service or employee!')
        raise SystemExit()

if __name__ == '__main__':
    main()