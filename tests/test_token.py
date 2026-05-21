import json
import requests
import users
from api.token import Token
from api.user import UserAPI
from config import Config
from users import ADMIN, User


class TestTokenPositive:
    def test_admin_token_positive(self, token_api: Token, random_user: User, user_api: UserAPI):
        response: requests.Response = token_api.get_token_raw(ADMIN)
        assert response.status_code == 200, f'Сервер ответил ошибкой: {response.status_code}'
        admin_token = response.json().get('token')
        assert admin_token, f'не пришёл токен'
        assert user_api.delete_raw(token=admin_token, id=random_user.id).status_code == 204, f'Админский токен невалидный'

    def test_get_token_via_login(self, token_api, random_user):
        new_user = random_user
        result = token_api.get_token_raw(new_user)
        assert result.status_code == 200
        token = result.json().get('token')
        assert token is not None
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{Config.url}/employees/all", headers=headers, params={"limit": 1})
        assert response.status_code == 200

    def test_get_token_from_deleted_user(self, random_user, token_api, admin_token):
        new_user = random_user
        client = UserAPI()
        client.delete_raw(token=admin_token, id = new_user.id)
        result = token_api.get_token_raw(new_user)
        assert result.status_code in (401, 404)

    def test_role_change_without_permission(self, random_user, token_api, admin_token, user_api):
        new_user_1 = random_user
        new_user_2 = random_user
        new_user_2_id = new_user_2.id

        new_user_1_token = token_api.get_token_raw(new_user_1).json().get('token')
        role_change = user_api.update_role_raw(new_user_1_token, new_user_2_id, 'admin')
        assert role_change.status_code == 403

    def test_get_token_without_password(self, token_api):
        created_user = User(login=  users.TEST.login, password= '')
        result = token_api.get_token_raw(created_user)
        assert result.status_code == 401
        assert not result.json().get('token')


    def test_get_token_without_login(self, token_api):
        created_user = User(login='', password = users.TEST.password)
        result = token_api.get_token_raw(created_user)
        assert result.status_code == 401
        assert not result.json().get('token')

    def test_get_token_with_invalid_login(self, token_api):
        created_user = User(login=users.TEST.login + 'a', password = users.TEST.password)
        result = token_api.get_token_raw(created_user)
        assert result.status_code == 401
        assert not result.json().get('token')

    def test_get_token_with_invalid_password(self, token_api):
        created_user = User(login=users.TEST.login, password = users.TEST.password + 'a')
        result = token_api.get_token_raw(created_user)
        assert result.status_code == 401
        assert not result.json().get('token')

    def test_get_token_without_user_data(self, token_api):
        user_data = {}
        result = requests.post(url=f"{Config.url}/token", json=user_data)
        assert result.status_code == 400

    def test_get_token_without_invalid_content_type(self, token_api, random_user):
        result = requests.post(url=f"{Config.url}/token", headers={'Content-Type': 'text/plain'}, data=json.dumps(random_user.dict()))
        assert result.status_code == 400

    def test_reusing_token_from_deleted_user(self, token_api, random_user, user_api, admin_token):
        user_token = token_api.get_token(random_user)
        user_api.delete_raw(token=admin_token, id=random_user.id)
        result = requests.get(f"{Config.url}/employees/all", headers={'Authorization': f'Bearer {user_token}'})
        assert result.status_code == 401





