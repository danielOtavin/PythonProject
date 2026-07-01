import pytest

from api.structure import StructureAPI
from models.employees import Employee

class TestStructure:
    @pytest.mark.parametrize("employee_count", [1, 5])
    def test_add_employee_to_company_and_get_employee_from_company(self, employee_count, random_employee, structure_api: StructureAPI,
                                     admin_token, random_company, employee_api, employee_cleanup):
        payload = []
        for _ in range(employee_count):
            employee_to_create = employee_api.create_employee(admin_token, Employee.random_employee())
            employee_cleanup(employee_to_create.id)
            payload.append(employee_to_create.id)
        response = structure_api.add_employee_to_company_raw(companyId=random_company.id, token=admin_token, employeeId=payload)
        assert response.status_code == 201
        response = structure_api.get_company_employees_raw(admin_token, random_company.id)
        assert response.status_code == 200


    @pytest.mark.parametrize("expected_company, expected_token, expected_employeeId, expected_status_code", [
        ('random_company', 'admin_token', -1, 400),
        ('random_company', 'admin_token', 0, 400),
        ('random_company', 'admin_token', [], 400),
        ('random_company', 'admin_token', ['1'], 400),
        ('random_company', 'empty_token', Employee.random_employee().id, 401),
        (-1, 'admin_token', Employee.random_employee().id, 400),
        (0, 'admin_token', Employee.random_employee().id, 400),
        ('1', 'admin_token', Employee.random_employee().id, 400),
        ('', 'admin_token', Employee.random_employee().id, 400),
        ('random_company', 'user_token', Employee.random_employee().id, 403),
    ])
    def test_add_employee_to_company_negative(self, expected_company, expected_token, expected_employeeId, expected_status_code, random_employee,
                                              structure_api: StructureAPI, admin_token, random_company, employee_api,
                                              user_token):
        tokens = {'admin_token': admin_token,
                  'user_token': user_token,
                  'empty_token': ''}

        token = tokens[expected_token]

        response = structure_api.add_employee_to_company_raw(companyId=random_company.id, token=token, employeeId=expected_employeeId)
        print(response.text)
        assert response.status_code == expected_status_code
