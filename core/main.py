import logging
import garobot as garobot_core
import api as garobot_api
import shop as garobot_shop
import scheduler as garobot_scheduler

def main():
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

    garobot.set_service(shop.get_service(service_id))
    garobot.set_employee(shop.get_employee(employee_id))
    garobot_scheduler.Scheduler(garobot, 60)

if __name__ == '__main__':
    main()