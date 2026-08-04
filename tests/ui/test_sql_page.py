from models.employees import Employee
from pages.sql_page import SQLPage

from allure import step

from models.users import ADMIN

from pytest import mark

@mark.sql
class TestEmployeesPage:
    @mark.parametrize('open_page', [(SQLPage, ADMIN)], indirect=True)
    def test_query_and_command_ui(self, admin_token, open_page: SQLPage, employee_api):
        with step('создать случайного сотрудника'):
            employee_data = Employee.random_employee()
            employee_create = employee_api.create_employee(admin_token, employee_data)

        with step('отправить запрос в базу'):
            open_page.send_sql_query(f'SELECT * FROM employee where id = {employee_create.id};')
            result_create = open_page.check_result(employee_create.id)

        with step('ID сотрудника содержится в базе'):
            assert str(employee_create.id) in result_create

        
        open_page.send_sql_command(f"DELETE FROM employee WHERE id = '{employee_create.id}';")
        open_page.send_sql_query('SELECT * FROM employee;')
        result_delete = open_page.check_result(employee_create.id)
        assert result_delete is False






