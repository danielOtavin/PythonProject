import pytest
from main import *


@ pytest.fixture(scope="session")
def employee_client():
    token = get_token()
    return Employee(token)