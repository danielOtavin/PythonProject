import pytest
import requests

from api.base import auth_headers
from config import Config
from employees import Employee


class EmployeeAPI:
    def create_raw(self, token: str, employee: Employee) -> requests.Response:
        return requests.post(f'{Config.url}/employees',
                             headers=auth_headers(token),
                             json=employee.dict())

    def create(self, token: str, employee: Employee) -> Employee:
        response = self.create_raw(token, employee)

        if response.status_code != 200:
            pytest.fail(reason=f"Сервeр ответил с ошибкой: {response.status_code}")

        if not (employee_raw := response.json()):
            pytest.fail(reason="Не пришёл ответ")

        return Employee.from_dict(employee_raw)


    def get_employees_all_raw(self, token: str, limit: int = 1) -> requests.Response:
        return requests.get(f'{Config.url}/employees/all',
                                headers=auth_headers(token),
                                params={'limit': limit})

    def get_employees(self, token: str, limit: int = 1):
        response = self.get_employees_all_raw(token, limit)
        if response.status_code != 200:
            pytest.fail(reason=f"сервeр ответил с ошибкой: {response.status_code}")

        employees_data = response.json()

        if not employees_data:
            pytest.fail(reason="не пришёл ответ")

        return [Employee.from_dict(emp) for emp in employees_data]


    def get_employee_raw(self, token: str, employeeId: int = 1) -> requests.Response:
        return requests.get(f'{Config.url}/employees/{employeeId}',
                            headers=auth_headers(token))

    def get_employee(self, token: str, employeeId: int = 1) -> Employee:
        response = self.get_employee_raw(token, employeeId)
        if response.status_code != 200:
            pytest.fail(reason=f"Сервeр ответил с ошибкой: {response.status_code}")

        if not (employee_raw := response.json()):
            pytest.fail(reason="Не пришёл ответ")

        return Employee.from_dict(employee_raw)

    def update_employee_raw(self, token: str, employeeId: int, employee: Employee) -> requests.Response:
        return requests.put(f'{Config.url}/employees/{employeeId}',
                            headers=auth_headers(token),
                            json= employee.dict()
                            )

    def update_employee(self,token: str, employeeId: int, employee: Employee) -> Employee:
        response = self.update_employee_raw(token, employeeId, employee)
        if response.status_code != 200:
            pytest.fail(reason=f"Сервeр ответил с ошибкой: {response.status_code}")

        if not (employee_raw := response.json()):
            pytest.fail(reason="Не пришёл ответ")

        return Employee.from_dict(employee_raw)

    def delete_employee_raw(self, token: str, employeeId: int) -> requests.Response:
        return requests.delete(f'{Config.url}/employees/{employeeId}',
                               headers=auth_headers(token))

    def delete_employee(self, token: str, employeeId: int):
        response = self.delete_employee_raw(token, employeeId)
        if response.status_code != 204:
            pytest.fail(reason=f"Сервeр ответил с ошибкой: {response.status_code}")

