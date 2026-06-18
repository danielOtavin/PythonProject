import pytest
from employees import Employee
from tests.conftest import admin_token


class TestEmployee:
    def test_crud_employee(self, employee_api, admin_token):
        new_employee_data = Employee.random_employee()
        response_create = employee_api.create_employee_raw(admin_token, new_employee_data)
        data_create = response_create.json()
        emp_id = data_create.get('id')
        assert response_create.status_code == 201
        assert data_create.pop('id') > 0
        assert data_create == {
            'name': new_employee_data.name,
            'salary': new_employee_data.salary,
            'work': new_employee_data.work
        }

        response_get = employee_api.get_employee_raw(token=admin_token, employeeId=emp_id)
        data_get = response_get.json()
        assert response_get.status_code == 200
        assert data_get.pop('id') == emp_id
        assert data_get == {
            'name': new_employee_data.name,
            'salary': new_employee_data.salary,
            'work': new_employee_data.work
        }

        updated_employee_data = Employee.random_employee()
        response_update = employee_api.update_employee_raw(admin_token, emp_id, updated_employee_data)
        assert response_update.status_code == 200
        assert response_update.json().get('id') == emp_id

        response_delete = employee_api.delete_employee_raw(admin_token, emp_id)
        assert response_delete.status_code == 204
        get_deleted_user = employee_api.get_employee_raw(admin_token, emp_id)
        assert get_deleted_user.status_code == 404
        second_delete = employee_api.delete_employee_raw(token=admin_token, employeeId=emp_id)
        assert second_delete.status_code == 404

    @pytest.mark.parametrize('expected_token, expected_status_code', [
        ('', 401),
        ('user_token', 403)
    ], ids= ['empty_token',
             'user_token'
             ])
    def test_create_employee_token_scenarios(self, random_employee, employee_api, user_token, expected_token, expected_status_code):
        token = '' if expected_token == 'empty' else user_token
        response = employee_api.create_employee_raw(token, random_employee)
        assert response.status_code == expected_status_code


    @pytest.mark.parametrize('employee_data, expected_status_code', [
        (lambda emp: Employee(name='', salary=emp.salary, work=emp.work), 400),
        (lambda emp: Employee(name=emp.name, salary=-1, work=emp.work), 400),
        (lambda emp: Employee(name=emp.name, salary=1_000_000_000, work=emp.work), 201),
        (lambda emp: {'name': Employee.random_employee().name, 'salary': '1_000_000_000', 'work': Employee.random_employee().work}, 400),
        (lambda emp: {'name': Employee.random_employee().name, 'work': Employee.random_employee().work}, 400),
        (lambda emp: {}, 400),
        (lambda emp: {'name': Employee.random_employee().name, 'salary': 1000, 'work': Employee.random_employee().work, 'extra_field': None}, 400)
        ],
        ids= ['empty_name',
              'negative_salary_value',
              'too_huge_salary_value',
              'incorrect_data_type',
              'without_required_field',
              'without_data',
              'with_extra_field'])
    def test_create_employee_with_employee_data(self, employee_api, admin_token, employee_data, expected_status_code, employee_cleanup):
        payload = employee_data(Employee.random_employee())
        response = employee_api.create_employee_raw(token=admin_token, custom_data=payload)
        assert response.status_code == expected_status_code
        employee_cleanup(response.json().get('id'))


    @pytest.mark.parametrize('expected_token, expected_employeeID, expected_status_code', [
        ('admin_token', 999999, 404),
        ('empty_token', 1, 401),
        ('user_token', 1, 200),
        ('admin_token', 'один', 404),
        ('admin_token', -1, 404),
    ],
        ids = ['unknown_id',
               'empty_token',
               'user_token',
               'invalid_data_type_in_id_field',
               'negative_id_number'])
    def test_get_employee(self, employee_api, admin_token, user_token, expected_token, expected_employeeID, expected_status_code):
        tokens = {'admin_token': admin_token,
                 'user_token': user_token,
                 'empty_token': ''}

        token = tokens[expected_token]

        response = employee_api.get_employee_raw(token, expected_employeeID)
        assert response.status_code == expected_status_code


    @pytest.mark.parametrize('expected_token, expected_employeeId, employee_data, expected_status_code', [
        ('admin_token', 'unknown_id', lambda emp: Employee(name=emp.name, salary=emp.salary, work=emp.work), 400),
        ('empty_token', 'id', lambda emp: Employee(name=emp.name, salary=emp.salary, work=emp.work), 401),
        ('user_token', 'id', lambda emp: Employee(name=emp.name, salary=emp.salary, work=emp.work), 403),
        ('admin_token', 'id', lambda emp: Employee(name='', salary=1000, work=True), 404),
        ('admin_token', 'id', lambda emp: Employee(name=emp.name, salary=-emp.salary, work=emp.work), 400),
        ('admin_token', 'id', {'name': Employee.random_employee().name, 'salary': '1000', 'work': Employee.random_employee().work}, 400),
        ('admin_token', 'id', {'name': Employee.random_employee().name, 'salary': Employee.random_employee().salary, 'work': Employee.random_employee().work, 'extra field': ''}, 404),
        ('admin_token', 'id', {}, 400)
    ],
        ids = ['unknown_id',
               'empty_token',
               'user_token',
               'empty_name_field',
               'negative_salary_field',
               'negative_data_type',
               'extra_field',
               'empty_data'
               ])
    def test_update_employee(self, admin_token, employee_api, expected_token, expected_employeeId, employee_data, expected_status_code,
                         user_token, random_employee):
        tokens = {'admin_token': admin_token,
                 'user_token': user_token,
                  'empty_token': ''}
        ids = {'id': random_employee.id,
               'unknown_id': 999999}
        token = tokens[expected_token]
        emp_id = ids[expected_employeeId]
        if callable(employee_data):
            employee_data = employee_data(random_employee)  # ← получаем Employee или dict
        response = employee_api.update_employee_raw(token, emp_id, employee_data)
        assert response.status_code == expected_status_code