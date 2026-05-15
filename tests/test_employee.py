from main import Employee


class TestEmployeePositive:
    def test_create_employee_positive(self, fake_employee_data, admin_auth):
        employee = Employee(admin_auth)
        result = employee.create_employee(fake_employee_data)
        assert result is not None
        assert isinstance(result, dict)
        assert 'id' in result
        assert 'name' in result
        assert 'salary' in result
        assert 'work' in result

    def test_update_employee_data(self, fake_employee_data, update_employee_data, admin_auth):
        client = Employee(admin_auth)
        employee = client.create_employee(fake_employee_data)
        old_id = employee.get('id')
        old_name = employee.get('name')
        old_salary = employee.get('salary')
        updated_employee = client.update_employee(old_id, update_employee_data)
        assert updated_employee.get('id') == old_id
        assert updated_employee.get('name') != old_name
        assert updated_employee.get('salary') != old_salary

    def test_delete_employee(self, fake_employee_data, admin_auth):
        employee = Employee(admin_auth)
        creation = employee.create_employee(fake_employee_data)
        employee_id = creation.get('id')
        assert employee.remove_employee(employee_id)
        assert employee.get_single_employee(employee_id) is None
