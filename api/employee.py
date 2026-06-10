import pytest
import requests

from api.base import auth_headers
from config import Config
from employees import Employee


class EmployeeAPI:
    def create(self, token: str, employee: Employee) -> Employee:
        response = self.create_raw(token, employee)

        if response.status_code != 201:
            pytest.fail(reason=f"Сервeр ответил с ошибкой: {response.status_code}")

        if not (employee_raw := response.json()):
            pytest.fail(reason="Не пришёл ответ")

        return Employee.model_validate(employee_raw)

    def create_raw(self, token: str, custom_data: dict | Employee) -> requests.Response:
        if isinstance(custom_data, Employee):
            payload = custom_data.model_dump()
        elif isinstance(custom_data, dict):
            payload = custom_data
        else:
            raise TypeError(f"custom_data должен быть Employee или dict, получен {type(custom_data)}")
        return requests.post(f'{Config.url}/employees',
                             headers=auth_headers(token),
                             json=payload)


    def get_employees_all_raw(self, token: str, limit: int = 1) -> requests.Response:
        return requests.get(f'{Config.url}/employees/all',
                                headers=auth_headers(token),
                                params={'limit': limit})

    def get_employees_all(self, token: str, limit: int = 1):
        response = self.get_employees_all_raw(token, limit)
        if response.status_code != 200:
            pytest.fail(reason=f"сервeр ответил с ошибкой: {response.status_code}")

        employees_data = response.json()

        if not employees_data:
            pytest.fail(reason="не пришёл ответ")

        return [Employee.model_validate(emp) for emp in employees_data]


    def get_employee_raw(self, token: str, employeeId: int = 1) -> requests.Response:
        return requests.get(f'{Config.url}/employees/{employeeId}',
                            headers=auth_headers(token))

    def get_employee(self, token: str, employeeId: int = 1) -> Employee:
        response = self.get_employee_raw(token, employeeId)
        if response.status_code != 200:
            pytest.fail(reason=f"Сервeр ответил с ошибкой: {response.status_code}")

        if not (employee_raw := response.json()):
            pytest.fail(reason="Не пришёл ответ")

        return Employee.model_validate(employee_raw)


    def update_employee(self,token: str, employeeId: int, new_employee_data: Employee) -> Employee:
        response = self.update_employee_raw(token, employeeId, new_employee_data)
        if response.status_code != 200:
            pytest.fail(reason=f"Сервeр ответил с ошибкой: {response.status_code}")

        if not (employee_raw := response.json()):
            pytest.fail(reason="Не пришёл ответ")

        return Employee.model_validate(employee_raw)

    def update_employee_raw(self, token: str, employeeId: int, custom_data: dict | Employee) -> requests.Response:
        if isinstance(custom_data, Employee):
            payload = custom_data.model_dump()
        elif isinstance(custom_data, dict):
            payload = custom_data
        else:
            raise TypeError(f"custom_data должен быть Employee или dict, получен {type(custom_data)}")
        return requests.put(f'{Config.url}/employees/{employeeId}',
                            headers=auth_headers(token),
                            json=payload)

    def delete_employee_raw(self, token: str, employeeId: int) -> requests.Response:
        return requests.delete(f'{Config.url}/employees/{employeeId}',
                               headers=auth_headers(token))

    def delete_employee(self, token: str, employeeId: int):
        response = self.delete_employee_raw(token, employeeId)
        if response.status_code != 204:
            pytest.fail(reason=f"Сервeр ответил с ошибкой: {response.status_code}")

