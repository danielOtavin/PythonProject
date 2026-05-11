import pytest
from main import *
import faker


@pytest.fixture(scope="function")
def fake_employee_data():
    fake = faker.Faker('ru_RU')
    return {'name': fake.name(),
            'salary': fake.random_int(1000, 2000),
            'work': fake.boolean()}

@pytest.fixture(scope="function")
def update_company_data(fake_employee_data):
    fake = faker.Faker('ru_RU')
    return {'name': fake.company(),
            'country': fake.country(),
            'year': fake.year()}