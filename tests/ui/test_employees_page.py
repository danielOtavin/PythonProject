import allure
import pytest

from dbase.data_base import TableName
from models.employees import Employee
from models.users import ADMIN
from pages.employees_page import EmployeePage
from pytest import mark

@mark.employees
class TestEmployeesPage:
    @pytest.mark.parametrize('open_page', [(EmployeePage, ADMIN)], indirect=True)
    def test_view_update_delete_employee_ui(self, clean_employees_db, open_page: EmployeePage, employee_api, admin_token,
                                            db):
        with allure.step('Создать сотрудника и просмотреть его данные в БД'):
            employee_data = Employee.random_employee()
            employee_created = employee_api.create_employee(admin_token, employee_data)
            open_page.page_refresh()
            open_page.wait_until_visible(open_page.EMPLOYEE_ITEM.format(emp_id=employee_created.id))
            result = open_page.view_employee_data(employee_created.id)
            assert employee_data.name in result
            open_page.close_modal_with_esc()

        with allure.step('Обновить данные сотрудника'):
            open_page.wait_until_visible(open_page.EMPLOYEE_ITEM.format(emp_id=employee_created.id))
            employee_updated_data = Employee.random_employee()
            open_page.update_employee_data(employee_created.id, employee_updated_data)
            open_page.close_modal_with_esc()

        with allure.step('Просмотреть данные сотрудника после обновления'):
            result2 = open_page.view_employee_data(employee_created.id)
            assert employee_updated_data.name in result2
            assert str(employee_updated_data.salary) in result2
            open_page.close_modal_with_esc()

        with allure.step('Удалить сотрудника и просмотреть данные о сотруднике в БД'):
            open_page.wait_until_visible(open_page.EMPLOYEE_ITEM.format(emp_id=employee_created.id))
            open_page.delete_employee_data(employee_created.id)
            assert db.check_object_in_db(TableName.EMPLOYEE, employee_data.id) == []
