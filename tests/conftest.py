from typing import Generator

import pytest

from api.company import CompanyAPI
from api.employee import EmployeeAPI
from api.token import Token
from api.user import UserAPI
from companies import Company
from employees import Employee
from users import ADMIN, TEST, User

@pytest.fixture(scope="session")
def token_api() -> Generator[Token]:
    yield Token()

@pytest.fixture(scope="session")
def user_api() -> Generator[UserAPI]:
    yield UserAPI()

@pytest.fixture(scope="session")
def employee_api() -> Generator[EmployeeAPI]:
    yield EmployeeAPI()

@pytest.fixture(scope="session")
def company_api() -> Generator[CompanyAPI]:
    yield CompanyAPI()


@pytest.fixture(scope='session')
def admin_token(token_api: Token) -> Generator[str]:
    yield token_api.get_token(user=ADMIN)


@pytest.fixture(scope='function', params=[TEST])
def user_token(request: pytest.FixtureRequest, token_api: Token):
    user = request.param
    return token_api.get_token(user=user)

@pytest.fixture(scope='function')
def random_user(user_api: UserAPI, admin_token: str) -> Generator[User]:
    user_to_create: User = User.random_user()
    user_created = user_api.create(user=user_to_create, token=admin_token)

    yield user_created
    
    user_api.delete_raw(token=admin_token, id=user_created.id)

@pytest.fixture(scope='function')
def random_employee(employee_api: EmployeeAPI, admin_token: str) -> Generator[Employee]:
    employee_to_create: Employee = Employee.random_employee()
    employee_created = employee_api.create(token=admin_token, employee=employee_to_create)

    yield employee_created

    employee_api.delete_employee_raw(token=admin_token, employeeId=employee_created.id)

@pytest.fixture(scope='function')
def random_company(company_api: CompanyAPI, admin_token: str) -> Generator[Company]:
    company_to_create: Company = Company.random_company()
    company_created = company_api.create(token=admin_token, company=company_to_create)

    yield company_created

    company_api.delete_company_raw(token=admin_token, companyId=company_to_create.id)

@pytest.fixture(params=['read', 'write', 'admin'])
def user_with_role(user_api: UserAPI, admin_token: str, request) -> Generator[User]:
    role = request.param
    user_to_create: User = User.random_user()
    user_created = user_api.create(user=user_to_create, token=admin_token)
    user_api.update_role(token=admin_token, role=role, userId=user_created.id)

    yield user_created

    user_api.delete_raw(token=admin_token, id=user_created.id)


@pytest.fixture(scope='function')
def employee_cleanup(employee_api: EmployeeAPI, admin_token: str):
    to_delete = []
    def add(employee_id):
        to_delete.append(employee_id)
    yield add
    for employee_id in to_delete:
        employee_api.delete_employee_raw(token=admin_token, employeeId=employee_id)

@pytest.fixture(scope='function')
def user_cleanup(user_api: UserAPI, admin_token: str):
    to_delete = []
    def add(user_id):
        to_delete.append(user_id)
    yield add
    for user_id in to_delete:
        user_api.delete_raw(token=admin_token, id=user_id)

@pytest.fixture(scope='function')
def company_cleanup(company_api: CompanyAPI, admin_token: str):
    to_delete = []
    def add(company_id):
        to_delete.append(company_id)
    yield add
    for company_id in to_delete:
        company_api.delete_company_raw(token=admin_token, companyId=company_id)












