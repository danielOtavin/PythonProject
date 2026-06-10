import pytest
import requests

from config import Config
from users import User


class Token:
    def get_token(self, user: User):
        response = self.get_token_raw(user=user)
        if response.status_code != 200:
            pytest.fail(reason=f"сервeр ответил с ошибкой: {response.status_code}")
            
        if not (token := response.json().get('token')):
            pytest.fail(reason="не пришёл токен")
                
        return token


    def get_token_raw(self, user: User) -> requests.Response:
        return requests.post(
             url=f"{Config.url}/token",
             json=user.model_dump(),
        )