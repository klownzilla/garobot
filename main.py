import logging
import core.garobot as garobot_core
import api.api as garobot_api
import core.shop as garobot_shop
import core.scheduler as garobot_scheduler

def main() -> None:
    logging.basicConfig(level=logging.INFO,
                        format='{asctime} :: {levelname} :: {funcName} :: {message}',
                        style='{',
                        handlers=[
                            logging.StreamHandler()
                        ])

    #TODO: make ids input
    business_id = 170649
    shop = garobot_shop.Shop()
    api = garobot_api.API()
    garobot = garobot_core.Garobot(shop, api, business_id)
    #ask shop here -> populate shop
    garobot.populate_shop()
    #show employees + services -> ask to enter -> set and populate appts
    service_id = 16663123
    employee_id = 44120875

    garobot.set_service(shop.get_service_by_id(service_id))
    garobot.set_employee(shop.get_employee_by_id(employee_id))
    garobot_scheduler.Scheduler(garobot, 60)

if __name__ == '__main__':
    main()