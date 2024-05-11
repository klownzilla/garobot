from __future__ import annotations
import json, logging

logger = logging.getLogger(__name__)

class Shop:
    def __init__(self) -> None:
        self.shop_services = set()
        self.shop_employees = set()

    def add_service(self, service: Service) -> None:
        self._get_services().add(service)

    def add_employee(self, employee: Employee) -> None:
        self._get_employees().add(employee)

    def _get_service(self, service_id: int) -> Service:
        services = self._get_services()
        for service in services:
            if service.get_service_id() == service_id:
                return service
        return Service(0, '', 0.0, '')

    def _get_services(self) -> set:
        return self.shop_services
    
    def _get_employees(self) -> set:
        return self.shop_employees
    
class Employee:
    def __init__(self, id: int, name: str) -> None:
        self.employee_id = id
        self.employee_name = name

    def get_employee_id(self) -> int:
        return self.employee_id
    
    def get_employee_name(self) -> str:
        return self.employee_name
    
    def __str__(self) -> str:
        obj_dict = {
            'employee_id':self.get_employee_id(),
            'employee_name':self.get_employee_name()
        }
        return json.dumps(obj_dict)

class Service:
    def __init__(self, id: int, name: str, price: float, description: str) -> None:
        self.service_id = id
        self.service_name = name
        self.service_price = price
        self.service_description = description

    def get_service_id(self) -> int:
        return self.service_id
    
    def get_service_name(self) -> str:
        return self.service_name
    
    def get_service_price(self) -> float:
        return self.service_price
    
    def get_service_description(self) -> str:
        return self.service_description
    
    def __str__(self) -> str:
        obj_dict = {
            'service_id':self.get_service_id(),
            'service_name':self.get_service_name(),
            'service_price':self.get_service_price(),
            'service_description':self.get_service_description()
        }
        return json.dumps(obj_dict)
