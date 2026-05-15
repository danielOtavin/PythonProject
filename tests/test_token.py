


import requests

from api.token import Token
from api.user import UserAPI
from users import ADMIN, User


class TestTokenPositive:
    def test_admin_token_positive(self, token_api: Token, random_user: User, user_api: UserAPI):
        response: requests.Response = token_api.get_token_raw(ADMIN)
        assert response.status_code == 200, f'Сервер ответил ошибкой: {response.status_code}'
        admin_token = response.json().get('token')
        assert admin_token, f'не пришёл токен'
        assert user_api.delete_raw(token=admin_token, id=random_user.id).status_code == 204, f'Админский токен невалидный'

