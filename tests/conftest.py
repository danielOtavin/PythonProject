import pytest
from main import *
import faker
from main import BASE_URL


@pytest.fixture(scope="module")
def fake_employee_data():
    fake = faker.Faker('ru_RU')
    return {'name': fake.name(),
            'salary': fake.random_int(1000, 2000),
            'work': fake.boolean()}

@pytest.fixture(scope="module")
def update_employee_data():
    fake = faker.Faker('ru_RU')
    return {'name': fake.name(),
            'salary': fake.random_int(1000, 2000),
            'work': fake.boolean()}

@pytest.fixture(scope="module")
def fake_company_data():
    fake = faker.Faker('ru_RU')
    return {'name': fake.company(),
            'country': fake.country(),
            'year': fake.year()}

@pytest.fixture(scope="module")
def update_company_data():
    fake = faker.Faker('ru_RU')
    return {'name': fake.company(),
            'country': fake.country(),
            'year': fake.year()}

@pytest.fixture(scope='session')
def admin_auth():
    admin = Token()
    return admin.get_token('admin', 'admin')

@pytest.fixture(scope='session')
def user_token():
    read_user = Token()
    return read_user.get_token('aaaa@mail.ru', '123456')