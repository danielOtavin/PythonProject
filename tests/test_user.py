import faker
import pytest


from tests.conftest import admin_token, token_api
from users import User, ERROR


class TestUserPositive:
    def test_create_user(self, admin_token, user_api):
        new_user = User.random_user()
        response = user_api.create_raw(new_user, admin_token)
        data = response.json()
        assert response.status_code == 201
        assert data['login'] == new_user.login
        assert data['id'] > 0



    @pytest.mark.parametrize("expected_token, expected_status_code, should_delete", [
        ('admin_token', 201, True),
        ('empty_token', 403, False),
        ('user_token', 403, False)
    ])
    def test_create_user_token(self, admin_token, user_token, random_user, user_api, expected_token, expected_status_code, should_delete):
        response = user_api.create_raw(random_user, expected_token)
        assert response == expected_status_code


    @pytest.mark.parametrize("user_data, expected_status_code", [
        (lambda u: User(login='', password=u.password), 400),
        (lambda u: User(login=u.login, password=''), 400),
        (lambda u: User(login=u.login, password=u.login), 400),
        (lambda u: User(login=u.login, password='1234567890'), 400),
        (lambda u: User(login=u.login, password='passwordwithoutdigits'), 400),
    ], ids= ['Пустой логин',
             'Пустой пароль',
             'Пароль и логин одинаковые',
             'Пароль содержит только цифры',
             'Пароль содержит только буквы'
             ])
    def test_create_user_data(self, admin_token, user_api, random_user, user_data, expected_status_code):
        payload = user_data(random_user)
        response = user_api.create_raw(payload, admin_token)
        assert response.status_code == expected_status_code


    def test_create_user_with_incorrect_login(self, random_user, user_api, admin_token):
        user_data = User(login=ERROR.login, password=User.random_user().password)
        response = user_api.create_raw(user_data, admin_token)
        assert response.status_code == 400


    def test_create_existing_user(self, user_api, admin_token, random_user):
        response = user_api.create_raw(random_user, admin_token)
        assert response.status_code == 409


    def test_create_existing_user_with_long_password(self, random_user, user_api, admin_token):
        fake = faker.Faker('ru_RU')
        user_data = User(login=User.random_user().login, password=fake.password(length=10000))
        response = user_api.create_raw(user_data, admin_token)
        assert response.status_code == 400


    def test_create_existing_user_with_short_password(self, random_user, user_api, admin_token):
        fake = faker.Faker('ru_RU')
        user_data = User(login=random_user.login, password=fake.password(length=5))
        response = user_api.create_raw(user_data, admin_token)
        assert response.status_code == 400



    def test_update_user_role(self, admin_token, user_api, random_user):
        response = user_api.create_raw(random_user, admin_token)
        created_role = response.json()['role']
        created_id = response.json()['id']
        user_updated_role = user_api.update_role_raw(token=admin_token, role = 'write', userId=created_id)
        assert user_updated_role.status_code == 200
        assert user_updated_role.json()['role'] != created_role

    def test_update_user_role_without_token(self, random_user, user_api):
        response = user_api.update_role_raw(token='', userId=random_user.id, role='write')
        assert response.status_code == 401

    def test_update_user_role_without_access(self, random_user, user_api, user_token):
        response = user_api.update_role_raw(token=user_token, userId=random_user.id, role='write')
        assert response.status_code == 403

    def test_update_unknown_user(self, admin_token, user_api):
        response = user_api.update_role_raw(token=admin_token, userId=999999, role='write')
        assert response.status_code == 404

    def test_update_user_invalid_role(self, admin_token, user_api, random_user):
        response = user_api.update_role_raw(token=admin_token, userId=random_user.id, role='админ')
        assert response.status_code == 400


    def test_user_can_change_own_password(self, admin_token, user_api, token_api):
        new_user = User.random_user()
        created_user = user_api.create(new_user, admin_token)

        user_token = token_api.get_token(created_user)

        new_password = "new_password_123"
        response = user_api.update_password_raw(created_user.id, user_token, new_password)
        assert response.status_code == 200

        updated_user = User(login=created_user.login, password=new_password)
        new_token = token_api.get_token(updated_user)
        assert new_token is not None

        user_api.delete(admin_token, created_user.id)
