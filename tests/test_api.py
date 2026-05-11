from main import *
import pytest

from tests.conftest import employee_client, fake_employee_data


class TestToken:
    def test_get_token(self):
        result = get_token()
        assert type(result) == str
        assert len(result) > 50

    def test_employee_client_is_employee_class(self, employee_client):
        assert isinstance(employee_client, Employee)

    def test_create_employee(self, employee_client, fake_employee_data):
        new_employee = employee_client.create_employee(fake_employee_data)

    def test_remove_employee(self, employee_client):
        employee_id = employee_client.create_employee()
        employee_client.remove_employee(employee_id)
        result = employee_client.get_single_employee(employee_id)
        assert result is None

    def test_update_employee(self, employee_client):
        employee_id = employee_client.create_employee()
        old_data = employee_client.get_single_employee(employee_id)
        result = employee_client.update_employee(employee_id)
        assert old_data['id'] == result['id']
        assert old_data['name'] != result['name']
        assert old_data['salary'] != result['salary']
        assert old_data['work'] != result['work']

