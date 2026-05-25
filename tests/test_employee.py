from http.client import responses

import requests

from api.base import auth_headers
from config import Config
from employees import Employee
from tests.conftest import admin_token


class TestEmployee:
    def test_create_employee(self, employee_api, random_employee, admin_token):
        response = employee_api.create_raw(token=admin_token, employee=random_employee)
        data = response.json()
        assert response.status_code == 201
        assert data.pop('id') > 0
        assert data == {
            'name': random_employee.name,
            'salary': random_employee.salary,
            'work': random_employee.work
        }

    def test_create_employee_without_token(self, random_employee, employee_api, admin_token):
        result = employee_api.create_raw(token='', employee=random_employee)
        assert result.status_code == 401

    def test_create_employee_with_user_token(self, random_employee, employee_api, user_token):
        result = employee_api.create_raw(token=user_token, employee=random_employee)
        assert result.status_code == 403

    def test_create_employee_without_name(self, random_employee, employee_api, admin_token):
        employee_data = Employee('', random_employee.salary, random_employee.work)
        result = employee_api.create_raw(token=admin_token, employee=employee_data)
        assert result.status_code == 400

    def test_create_employee_with_negative_salary(self, random_employee, employee_api, admin_token):
        employee_data = Employee(random_employee.name, -1, random_employee.work)
        result = employee_api.create_raw(token=admin_token, employee=employee_data)
        assert result.status_code == 400

    def test_create_employee_without_required_field(self, random_employee, employee_api, admin_token):
        employee_data = {'name': random_employee.name, 'work': random_employee.work}
        headers = auth_headers(admin_token)
        result = requests.post(f'{Config.url}/employees', headers=headers ,json=employee_data)
        assert result.status_code == (400, 422)

    def test_create_employee_with_huge_salary(self, random_employee, employee_api, admin_token):
        employee_data = Employee(random_employee.name,
                                 1_000_000_000,
                                 random_employee.work)
        result = employee_api.create_raw(token=admin_token, employee=employee_data)
        assert result.status_code == 201
        employee_api.delete_employee_raw(token=admin_token, employeeId=result.json().get('id'))

    def test_create_employee_with_incorrect_field_type(self, random_employee, employee_api, admin_token):
        employee_data = Employee(random_employee.name,
                                 'сто тыщ мильонов косарей',
                                 random_employee.work)
        result = employee_api.create_raw(token=admin_token, employee=employee_data)
        assert result.status_code == 400


    def test_create_employee_without_data(self, random_employee, employee_api, admin_token):
        employee_data = {}
        headers = auth_headers(admin_token)
        result = requests.post(f'{Config.url}/employees', headers=headers, json=employee_data)
        assert result.status_code == 400

    def test_create_employee_with_extra_field(self, random_employee, employee_api, admin_token):
        employee_data = {'name': random_employee.name,
                         'salary': 1000,
                         'work': random_employee.work,
                         'extra_field': 'a'}
        headers = auth_headers(admin_token)
        result = requests.post(f'{Config.url}/employees', headers=headers ,json=employee_data)
        assert result.status_code == (400, 422)


    def test_get_employee_by_id(self, employee_api, random_employee, admin_token):
        created_employee = employee_api.create(token=admin_token, employee=random_employee)
        response = employee_api.get_employee_raw(token=admin_token, employeeId=created_employee.id)
        data = response.json()
        assert response.status_code == 200
        assert data.pop('id') == created_employee.id
        assert data == {
            'name': random_employee.name,
            'salary': random_employee.salary,
            'work': random_employee.work
        }

    def test_get_employee_with_unknown_id(self, employee_api, admin_token):
        response = employee_api.get_employee_raw(token=admin_token, employeeId=9999999)
        assert response.status_code == 404

    def test_get_employee_without_authorization(self, employee_api, admin_token):
        result = employee_api.get_employee_raw(token='')
        assert result.status_code == 401

    def test_get_employee_with_user_token(self, employee_api, user_token):
        result = employee_api.get_employee_raw(token=user_token)
        assert result.status_code == 200

    def test_get_employee_with_str_type_id(self, employee_api, admin_token):
        result = employee_api.get_employee_raw(token=admin_token, employeeId='1')
        assert result.status_code == 404

    def test_get_employee_with_incorrect_id(self,employee_api, admin_token):
        result = employee_api.get_employee_raw(token=admin_token, employeeId=-1)
        assert result.status_code == 404


    def test_update_user(self, employee_api, random_employee, admin_token):
        new_data = Employee.random_employee()
        response = employee_api.update_employee_raw(token=admin_token, employeeId=random_employee.id, employee=new_data)
        assert response.status_code == 200
        assert random_employee.id == response.json().get('id')

    def test_update_unknown_employee(self, employee_api, admin_token):
        employee_data = Employee('Ivan', 1000, True)
        result = employee_api.update_employee_raw(token=admin_token,
                                                  employeeId=9999999,
                                                  employee=employee_data)
        assert result.status_code == 404

    def test_update_user_without_token(self, employee_api, admin_token, random_employee):
        employee_data = Employee('Ivan', 1000, True)
        result = employee_api.update_employee_raw(token='',
                                                  employeeId=9999999,
                                                  employee=employee_data)
        assert result.status_code == 401

    def test_update_user_without_access(self, employee_api, user_token, random_employee, admin_token):
        employee_data = Employee('Ivan', 1000, True)
        result = employee_api.update_employee_raw(token=user_token, employeeId=random_employee.id, employee=employee_data)
        assert result.status_code == 403

    def test_update_user_without_name(self, employee_api, admin_token, random_employee):
        employee_data = Employee('', 1000, True)
        result = employee_api.update_employee_raw(token=admin_token, employeeId=random_employee.id, employee=employee_data)
        assert result.status_code == 404

    def test_update_user_with_negative_salary(self, employee_api, admin_token, random_employee):
        employee_data = Employee('Ivan', -1000, True)
        result = employee_api.update_employee_raw(token=admin_token,employeeId=random_employee.id, employee=employee_data)
        assert result.status_code == 404

    def test_update_user_with_incorrect_field_type(self, employee_api, admin_token, random_employee):
        employee_data = Employee('Ivan', 'двести лямов', True)
        result = employee_api.update_employee_raw(token=admin_token,
                                                  employeeId=random_employee.id,
                                                  employee=employee_data)
        assert result.status_code == 404

    def test_update_user_with_extra_field(self, employee_api, admin_token, random_employee):
        employee_data = {'name': 'Ivan', 'salary': 1000, 'work': True, 'extra_field': 'a'}
        headers = auth_headers(admin_token)
        result = requests.put(f'{Config.url}/employees/{random_employee.id}', headers=headers, json=employee_data)
        assert result.status_code == 400



    def test_delete_created_user(self, employee_api, random_employee, admin_token):
        created_user = employee_api.create(token=admin_token, employee=random_employee)
        get_before = employee_api.get_employee_raw(token=admin_token, employeeId=created_user.id)
        assert get_before.status_code == 200
        response = employee_api.delete_employee_raw(token=admin_token, employeeId=created_user.id)
        assert response.status_code == 204
        find_deleted_user = employee_api.get_employee_raw(token=admin_token, employeeId=created_user.id)
        assert find_deleted_user.status_code == 404
        second_delete = employee_api.delete_employee_raw(token=admin_token, employeeId=created_user.id)
        assert second_delete.status_code == 404
