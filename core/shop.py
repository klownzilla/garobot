from __future__ import annotations
from datetime import datetime
import json

class Shop:
    def __init__(self) -> None:
        self.shop_services = set()
        self.shop_employees = set()
        self.shop_appointments = []

    def add_service(self, service: Service) -> None:
        self._get_services().add(service)

    def add_employee(self, employee: Employee) -> None:
        self._get_employees().add(employee)

    def add_appointment(self, appointment: Appointment) -> None:
        self.get_appointments().append(appointment)

    def get_service(self, service_id: int) -> Service:
        services = self._get_services()
        for service in services:
            if service.get_service_id() == service_id:
                return service
        return Service(0, '', 0, '')
    
    def get_employee(self, employee_id: int) -> Employee:
        employees = self._get_employees()
        for employee in employees:
            if employee.get_employee_id() == employee_id:
                return employee
        return Employee(0, '')
    
    def get_appointment(self, appointment_date_time: datetime) -> Appointment:
        appointments = self.get_appointments()
        for appointment in appointments:
            if appointment.get_appointment_date_time() == appointment_date_time:
                return appointment
        return Appointment(0, datetime(2000, 1, 1), Service(0, '', 0, ''), Employee(0, ''))

    def _get_services(self) -> set:
        return self.shop_services
    
    def _get_employees(self) -> set:
        return self.shop_employees
    
    def get_appointments(self) -> list:
        return self.shop_appointments
    
class Employee:
    def __init__(self, id: int, name: str) -> None:
        self.employee_id = id
        self.employee_name = name
        self.appointments = set()

    def get_employee_id(self) -> int:
        return self.employee_id
    
    def get_employee_name(self) -> str:
        return self.employee_name
    
    def get_appointments(self) -> set[Appointment]:
        return self.appointments
    
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
    
class Appointment:
    def __init__(self, appointment_id: int, appointment_date_time: datetime, service: Service, employee: Employee) -> None:
        self.appointment_id = appointment_id
        self.appointment_date_time = appointment_date_time
        self.service = service
        self.employee = employee

    def get_appointment_id(self) -> int:
        return self.appointment_id
    
    def get_appointment_date_time(self) -> datetime:
        return self.appointment_date_time
    
    def get_appointment_service(self) -> Service:
        return self.service
    
    def get_appointment_employee(self) -> Employee:
        return self.employee
    
    def __str__(self) -> str:
        obj_dict = {
            'appointment_id':self.get_appointment_id(),
            'appointment_date':str(self.get_appointment_date_time()),
        }
        return json.dumps(obj_dict)

