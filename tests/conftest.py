import pytest
from api.company import CompanyAPI
from api.employee import EmployeeAPI
from api.structure import StructureAPI
from api.token import Token
from api.user import UserAPI
from models.companies import Company
from models.employees import Employee
from models.users import ADMIN, TEST, User

@pytest.fixture(scope="session")
def token_api():
    yield Token()

@pytest.fixture(scope="session")
def user_api():
    yield UserAPI()

@pytest.fixture(scope="session")
def employee_api():
    yield EmployeeAPI()

@pytest.fixture(scope="session")
def company_api():
    yield CompanyAPI()

@pytest.fixture(scope="session")
def structure_api():
    yield StructureAPI()

@pytest.fixture(scope='session')
def admin_token(token_api: Token):
    yield token_api.get_token(user=ADMIN)


@pytest.fixture(scope='function')
def user_token(request: pytest.FixtureRequest, token_api: Token) -> Token:
    return token_api.get_token(user=TEST)

@pytest.fixture(scope="session", autouse=True)
def ensure_test_user(admin_token, user_api, token_api):
    response = token_api.get_token_raw(TEST)
    if response.status_code != 200:
        user_api.create(TEST, admin_token)


@pytest.fixture(scope='function')
def random_user(user_api: UserAPI, admin_token: str) -> User:
    user_to_create: User = User.random_user()
    user_created = user_api.create(user=user_to_create, token=admin_token)

    yield user_created
    
    user_api.delete_raw(token=admin_token, id=user_created.id)

@pytest.fixture(scope='function')
def random_employee(employee_api: EmployeeAPI, admin_token: str):
    employee_to_create: Employee = Employee.random_employee()
    employee_created = employee_api.create_employee(token=admin_token, employee=employee_to_create)

    yield employee_created

    employee_api.delete_employee_raw(token=admin_token, employeeId=employee_created.id)

@pytest.fixture(scope='function')
def random_company(company_api: CompanyAPI, admin_token: str):
    company_to_create: Company = Company.random_company()
    company_created = company_api.create_company(token=admin_token, company=company_to_create)

    yield company_created

    company_api.delete_company_raw(token=admin_token, companyId=company_created.id)

@pytest.fixture(params=['read', 'write', 'admin'])
def user_with_role(user_api: UserAPI, admin_token: str, request):
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
    for emp_id in to_delete:
        employee_api.delete_employee_raw(token=admin_token, employeeId=emp_id)

@pytest.fixture(scope='function')
def user_cleanup(user_api: UserAPI, admin_token: str):
    to_delete = []
    def add(user_id):
        to_delete.append(user_id)
    yield add
    for usr_id in to_delete:
        user_api.delete_raw(token=admin_token, id=usr_id)

@pytest.fixture(scope='function')
def company_cleanup(company_api: CompanyAPI, admin_token: str):
    to_delete = []
    def add(company_id):
        to_delete.append(company_id)
    yield add
    for cmp_id in to_delete:
        company_api.delete_company_raw(token=admin_token, companyId=cmp_id)