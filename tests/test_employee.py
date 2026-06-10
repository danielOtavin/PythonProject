import pytest

from employees import Employee
from tests.conftest import admin_token, user_token

class TestEmployee:
    def test_create_employee(self, employee_api, random_employee, admin_token):
        response = employee_api.create_raw(admin_token, random_employee)
        data = response.json()
        assert response.status_code == 201
        assert data.pop('id') > 0
        assert data == {
            'name': random_employee.name,
            'salary': random_employee.salary,
            'work': random_employee.work
        }


    @pytest.mark.parametrize('expected_token, expected_status_code', [
        ('empty', 401),
        ('user_token', 403)
    ])
    def test_create_employee_token_scenarios(self, random_employee, employee_api, user_token, expected_token, expected_status_code):
        token = '' if expected_token == 'empty' else user_token
        response = employee_api.create_raw(token, random_employee)
        assert response.status_code == expected_status_code


    @pytest.mark.parametrize('employee_data, expected_status_code', [
        (lambda emp: Employee(name='', salary=emp.salary, work=emp.work), 400),
        (lambda emp: Employee(name=emp.name, salary=-1, work=emp.work), 400),
        (lambda emp: Employee(name=emp.name, salary=1_000_000_000, work=emp.work), 201),
        (lambda emp: Employee(name=emp.name, salary='1_000_000_000', work=emp.work), 400),
    ],
        ids= ['без имени',
              'отрицательное значение зарплаты',
              'слишком большое значение зарплаты',
              'неправильный тип данных'])
    def test_create_employee_with_employee_data(self, random_employee, employee_api, admin_token, employee_data, expected_status_code, employee_cleanup):
        payload = employee_data(random_employee)
        response = employee_api.create_raw(token=admin_token, custom_data=payload)
        assert response.status_code == expected_status_code
        employee_cleanup(response.json().get('id'))

    def test_create_employee_without_required_field(self, random_employee, employee_api, admin_token):
        employee_data = {'name': random_employee.name, 'work': random_employee.work}
        response = employee_api.create_raw(admin_token, employee_data)
        assert response.status_code == (400, 422)


    def test_create_employee_without_data(self, random_employee, employee_api, admin_token):
        employee_data = {}
        response = employee_api.create_raw(admin_token, employee_data)
        assert response.status_code == 400


    def test_create_employee_with_extra_field(self, random_employee, employee_api, admin_token):
        employee_data = {'name': random_employee.name,
                         'salary': 1000,
                         'work': random_employee.work,
                         'extra_field': None}
        response = employee_api.create_raw(admin_token, employee_data)
        assert response.status_code == 400


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


    @pytest.mark.parametrize('expected_token, expected_employeeID, expected_status_code', [
        ('admin_token', 999999, 404),
        ('empty_token', 1, 401),
        ('user_token', 1, 200),
        ('admin_token', '1', 404),
        ('admin_token', -1, 404),
    ])
    def test_get_employee(self, employee_api, admin_token, user_token, expected_token, expected_employeeID, expected_status_code):
        tokens = {'admin_token': admin_token,
                 'user_token': user_token,
                 'empty_token': ''}

        token = tokens[expected_token]

        response = employee_api.get_employee_raw(token, expected_employeeID)
        assert response.status_code == expected_status_code


    @pytest.mark.parametrize('expected_token, expected_employeeId, expected_status_code', [
        ('admin_token', 999999, 404),
        ('empty_token', 1, 401),
        ('user_token', 1, 403)
    ])
    def test_update_employee(self, admin_token, employee_api, expected_token, expected_employeeId, expected_status_code,
                         user_token):
        tokens = {'admin_token': admin_token,
                 'user_token': user_token,
                  'empty_token': ''}

        token = tokens[expected_token]

        response = employee_api.update_employee_raw(token, expected_employeeId, Employee(name='Ivan', salary=1000, work=True))
        assert response.status_code == expected_status_code


    def test_successful_update_employee(self, employee_api, random_employee, admin_token):
        new_data = Employee.random_employee()
        response = employee_api.update_employee_raw(admin_token, random_employee.id, new_data)
        assert response.status_code == 200
        assert random_employee.id == response.json().get('id')


    @pytest.mark.parametrize('employee_data, expected_status_code', [
        (Employee(name='', salary=1000, work=True), 404),
        (Employee(name='Ivan', salary=-1000, work=True), 404),
        (Employee(name='Ivan', salary='1000', work=True), 404),
        ({'name': 'Ivan', 'salary': 1000, 'work': True, 'extra_field': ''}, 400)
    ])
    def test_update_user_incorrect_data_or_extra_field(self, employee_api, admin_token, random_employee, employee_data, expected_status_code):
        response = employee_api.update_employee_raw(token=admin_token, employeeId=random_employee.id, custom_data=employee_data)
        assert response.status_code == expected_status_code



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
