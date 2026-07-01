import pytest
import requests
from pydantic import BaseModel

from api.base import auth_headers
from config import Config
from models.employees import Employee


class EmployeesRequest(BaseModel):
    class EmployeeInCompany(BaseModel):
        id: int
    employees: list[EmployeeInCompany]


class StructureAPI:
    def get_company_employees(self, token: str, companyId: int):
        response = self.get_company_employees_raw(companyId, token)
        if response.status_code != 200:
            pytest.fail(reason=f"Сервeр ответил с ошибкой: {response.status_code}")

        company_employees_data = response.json()

        if not company_employees_data:
            pytest.fail(reason="не пришёл ответ")

        return [Employee.model_validate(emp) for emp in company_employees_data]


    def get_company_employees_raw(self, companyId: int, token: str):
        return requests.get(Config.url + f'/structure/{companyId}',
                                headers=auth_headers(token))


    def _build_payload(self, employeeId: int| list):
        if isinstance(employeeId, int):
            payload = [employeeId]
        elif isinstance(employeeId, list):
            payload = employeeId
        else:
            raise TypeError(f'employeeId должен быть int или dict, получен {type(employeeId)}')
        return payload


    def add_employee_to_company_raw(self, companyId: int, token: str, employeeId: int | list) -> requests.Response:
        payload = self._build_payload(employeeId)
        return requests.post(Config.url + f'/structure/{companyId}',
                             headers=auth_headers(token),
                             json=payload)


    def delete_employee_from_company(self, companyId: int, token: str, employeeId: int | list):
        response = self.delete_employee_from_company_raw(companyId, token, employeeId)

        if response.status_code != 204:
            pytest.fail(reason=f"Сервeр ответил с ошибкой: {response.status_code}")


    def delete_employee_from_company_raw(self, companyId: int, token: str, employeeId: int | list) -> requests.Response:
        payload = self._build_payload(employeeId)
        return requests.delete(Config.url + f'/structure/{companyId}',
                               headers=auth_headers(token),
                               json=payload)