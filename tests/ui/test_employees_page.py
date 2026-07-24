from models.employees import Employee
from pages.employees_page import EmployeePage


class TestEmployeesPage:
    def test_view_update_delete_employee_ui(self, browser, clean_table_db, pages_admin_token, employee_api, admin_token,
                                         db_check_obj):
        clean_table_db('employee')
        employee_data = Employee.random_employee()
        employee_created = employee_api.create_employee(admin_token, employee_data)
        employee_page = pages_admin_token(EmployeePage)

        employee_page.wait_until_visible(employee_page.get_employee_item(employee_created.id))
        result = employee_page.view_employee_data(employee_created.id)
        assert employee_data.name in result
        employee_page.close_modal_with_esc()


        employee_page.wait_until_visible(employee_page.get_employee_item(employee_created.id))
        employee_updated_data = Employee.random_employee()
        employee_page.update_employee_data(employee_created.id, employee_updated_data)
        employee_page.close_modal_with_esc()

        result2 = employee_page.view_employee_data(employee_created.id)
        assert employee_updated_data.name in result2
        employee_page.close_modal_with_esc()

        employee_page = pages_admin_token(EmployeePage)
        employee_page.wait_until_visible(employee_page.get_employee_item(employee_created.id))
        employee_page.delete_employee_data(employee_created.id)
        assert db_check_obj('employee', employee_data.name) == []
