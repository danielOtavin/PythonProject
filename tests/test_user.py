from http.client import responses

from api.token import Token
from api.user import UserAPI
from tests.conftest import admin_token
from users import User


class TestUserPositive:
    def test_create_and_delete_user(self, admin_token, user_api):
        user_data = User.random()

        response = user_api.create_raw(user_data)
        data = response.json()
        assert response.status_code == 200
        '''Почему тут приходит код 200, а в сваггере 201 должен быть?'''
        assert data['login'] == user_data.login
        assert data['id'] > 0

        delete_user = user_api.delete_raw(token=admin_token, id = data['id'])
        assert delete_user.status_code == 204


    def test_user_role_change(self, admin_token, user_api, random_user):
        response = user_api.create_raw(random_user)
        created_role = response.json()['role']
        created_id = response.json()['id']
        user_updated_role = user_api.update_role_raw(token=admin_token, role = 'write', userId=created_id)
        assert user_updated_role.status_code == 200
        assert user_updated_role.json()['role'] != created_role




