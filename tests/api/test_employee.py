import allure
import pytest
from employees import Employee


@allure.feature('Employee API')
class TestEmployee:
    @allure.story('Create employee')
    @allure.title('Test CRUD employee')
    def test_crud_employee(self, employee_api, admin_token):
        with allure.step('Создать данные работника'):
            new_employee_data = Employee.random_employee()
        with allure.step('Отправить запрос на создание сотрудника'):
            response_create = employee_api.create_employee_raw(admin_token, new_employee_data)
        with allure.step('Десериализировать ответ сервера'):
            data_create = response_create.json()
        with allure.step('Получить ID сотрудника'):
            emp_id = data_create.get('id')
        with allure.step('Проверить статус код ответа сервера'):
            assert response_create.status_code == 201
        with allure.step('Проверить значение ID больше нуля'):
            assert data_create.pop('id') > 0
        with allure.step('Проверить соответствие данных созданного сотрудника ожидаемым данным'):
            assert data_create == {
                'name': new_employee_data.name,
                'salary': new_employee_data.salary,
                'work': new_employee_data.work
            }
        with allure.step('Отправить запрос на получение сотрудника'):
            response_get = employee_api.get_employee_raw(token=admin_token, employeeId=emp_id)
        with allure.step('Десериализировать ответ сервера'):
            data_get = response_get.json()
        with allure.step('Проверить статус код ответа сервера'):
            assert response_get.status_code == 200
        with allure.step('Проверить соответствие полученного ID'):
            assert data_get.pop('id') == emp_id
        with allure.step('Проверить соответствие данных полученного сотрудника ожидаемым данным'):
            assert data_get == {
                'name': new_employee_data.name,
                'salary': new_employee_data.salary,
                'work': new_employee_data.work
            }
        with allure.step('Создать данные для обновления данных работника'):
            updated_employee_data = Employee.random_employee()
        with allure.step('Отправить запрос на обновление данных сотрудника'):
            response_update = employee_api.update_employee_raw(admin_token, emp_id, updated_employee_data)
        with allure.step('Проверить статус код ответа сервера'):
            assert response_update.status_code == 200
        with allure.step('Проверить соответствие полученного ID'):
            assert response_update.json().get('id') == emp_id

        with allure.step('Отправить запрос на удаление сотрудника'):
            response_delete = employee_api.delete_employee_raw(admin_token, emp_id)
        with allure.step('Проверить статус код ответа сервера'):
            assert response_delete.status_code == 204
        with allure.step('Отправить запрос на получение удаленного сотрудника'):
            get_deleted_user = employee_api.get_employee_raw(admin_token, emp_id)
        with allure.step('Проверить статус код ответа сервера'):
            assert get_deleted_user.status_code == 404
        with allure.step('Отправить запрос на повторное удаление сотрудника'):
            second_delete = employee_api.delete_employee_raw(token=admin_token, employeeId=emp_id)
        with allure.step('Проверить статус код ответа сервера'):
            assert second_delete.status_code == 404

    @pytest.mark.parametrize('expected_token, expected_status_code', [
        ('', 401),
        ('user_token', 403)
    ], ids= ['empty_token',
             'user_token'
             ])
    @allure.story('Создание сотрудника')
    @allure.title('Создание сотрудника с использованием различных токенов')
    def test_create_employee_token_scenarios(self, random_employee, employee_api, user_token, expected_token, expected_status_code):
        with allure.step('Подобрать подходящий для теста токен'):
            token = '' if expected_token == 'empty' else user_token
        with allure.step('Отправить запрос на создание сотрудника с использованием определенного токена'):
            response = employee_api.create_employee_raw(token, random_employee)
        with allure.step('Проверить статус код ответа сервера'):
            assert response.status_code == expected_status_code


    @pytest.mark.parametrize('employee_data, expected_status_code', [
        (lambda emp: {'name': Employee.random_employee().name, 'salary': '1_000_000_000', 'work': Employee.random_employee().work}, 400),
        (lambda emp: {'name': Employee.random_employee().name, 'work': Employee.random_employee().work}, 400),
        (lambda emp: {}, 400),
        (lambda emp: {'name': Employee.random_employee().name, 'salary': Employee.random_employee().salary, 'work': Employee.random_employee().work, 'extra_field': None}, 400)
        ],
        ids= ['incorrect_data_type',
              'without_required_field',
              'without_data',
              'with_extra_field'])
    @allure.story('Создание сотрудника')
    @allure.title('Создание сотрудника с использованием данных типа dict')
    def test_create_employee_with_data_dict(self, employee_api, admin_token, employee_data, expected_status_code, employee_cleanup):
        with allure.step('Подготовка данных для запроса'):
            payload = employee_data(Employee.random_employee())
        with allure.step('Отправить запрос на создание сотрудника'):
            response = employee_api.create_employee_raw(token=admin_token, custom_data=payload)
        with allure.step('Проверить статус код ответа сервера'):
            assert response.status_code == expected_status_code
        with allure.step('Удалить созданного сотрудника из БД'):
            employee_cleanup(response.json().get('id'))


    @pytest.mark.parametrize('employee_data, expected_status_code', [
        (lambda emp: Employee(name='', salary=emp.salary, work=emp.work), 400),
        (lambda emp: Employee(name=emp.name, salary=-1, work=emp.work), 400),
        (lambda emp: Employee(name=emp.name, salary=1_000_000_000, work=emp.work), 201)
    ],
        ids=['empty_name',
             'negative_salary_value',
             'too_huge_salary_value'])
    @allure.story('Создание сотрудника')
    @allure.title('Создание сотрудника с использованием данных типа Employee')
    def test_create_employee_with_data_employee(self, employee_api, admin_token, employee_data, expected_status_code, employee_cleanup):
        with allure.step('Подготовка данных для запроса'):
            payload = employee_data(Employee.random_employee())
        with allure.step('Отправить запрос на создание сотрудника'):
            response = employee_api.create_employee_raw(token=admin_token, custom_data=payload)
        with allure.step('Проверить статус код ответа сервера'):
            assert response.status_code == expected_status_code
        with allure.step('Удалить созданного сотрудника из БД'):
            employee_cleanup(response.json().get('id'))


    @pytest.mark.parametrize('expected_token, expected_employeeID, expected_status_code', [
        ('admin_token', 999999, 404),
        ('empty_token', 1, 401),
        ('user_token', 1, 200),
        ('admin_token', '1', 404),
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
            employee_data = employee_data(random_employee)
        response = employee_api.update_employee_raw(token, emp_id, employee_data)
        assert response.status_code == expected_status_code