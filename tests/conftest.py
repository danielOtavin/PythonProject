from typing import Generator

import pytest
from api.token import Token
import faker
from api.user import UserAPI
from users import ADMIN, TEST, User


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

@pytest.fixture(scope="session")
def token_api() -> Generator[Token]:
    yield Token()

@pytest.fixture(scope="session")
def user_api() -> Generator[UserAPI]:
    yield UserAPI()


@pytest.fixture(scope='session')
def admin_token(token_api: Token) -> Generator[str]:
    yield token_api.get_token(user=ADMIN)


@pytest.fixture(scope='function', params=[TEST])
def user_token(request: pytest.FixtureRequest, token_api: Token):
    user = request.param
    return token_api.get_token(user=user)

@pytest.fixture(scope='function')
def random_user(user_api: UserAPI, admin_token: str) -> Generator[User]:
    user_to_create: User = User.random()
    user_created = user_api.create(user=user_to_create)

    yield user_created
    
    user_api.delete_raw(token=admin_token, id=user_created.id)