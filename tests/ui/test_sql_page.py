from models.employees import Employee


class TestEmployeesPage:
    def test_query_and_command_ui(self, admin_token, page_specific_admin_token, employee_api):
        employee_data = Employee.random_employee()
        employee_create = employee_api.create_employee(admin_token, employee_data)
        sql_page = page_specific_admin_token('SQLPage')
        sql_page.send_sql_query('SELECT * FROM employee;')
        result_create = sql_page.check_result(employee_create.id)
        assert str(employee_create.id) in result_create
        sql_page.send_sql_command(f"DELETE FROM employee WHERE id = '{employee_create.id}';")
        sql_page.send_sql_query('SELECT * FROM employee;')
        result_delete = sql_page.check_result(employee_create.id)
        assert result_delete is False






