import requests
from pydantic import BaseModel

from api.base import auth_headers
from config import Config


class EmployeesRequest(BaseModel):
    class EmployeeInCompany(BaseModel):
        id: int
    employees: list[EmployeeInCompany]

class StructureAPI:
    def get_company_employees_raw(self, companyId: int, token: str):
        return requests.get(Config.url + f'/structure/{companyId}',
                                headers=auth_headers(token))

    def _build_payload(self, employeeId: int| list):
        if isinstance(employeeId, int):
            result = EmployeesRequest(employees=[EmployeesRequest.EmployeeInCompany(id=employeeId)])
            payload = result.model_dump()
        elif isinstance(employeeId, list):
            result = EmployeesRequest(employees=[EmployeesRequest.EmployeeInCompany(id=e) for e in employeeId])
            payload = result.model_dump()
        else:
            raise TypeError(f'employeeId должен быть int или dict, получен {type(employeeId)}')
        return payload

    def add_employee_to_company_raw(self, companyId: int, token: str, employeeId: int | list) -> requests.Response:
        payload = self._build_payload(employeeId)
        return requests.post(Config.url + f'/structure/{companyId}',
                             headers=auth_headers(token),
                             json=payload)

    def delete_employee_from_company_raw(self, companyId: int, token: str, employeeId: int | list) -> requests.Response:
        payload = self._build_payload(employeeId)
        return requests.delete(Config.url + f'/structure/{companyId}',
                               headers=auth_headers(token),
                               json=payload)