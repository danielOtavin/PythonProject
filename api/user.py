import pytest
import requests

from config import Config
from users import User
from api.base import auth_headers


class UserAPI:
    def create(self, user: User) -> User:
        response = self.create_raw(user=user)
        
        if response.status_code != 200:
            pytest.fail(reason=f"сервeр ответил с ошибкой: {response.status_code}")
            
        if not (user_raw := response.json()):
            pytest.fail(reason="не пришёл ответ")

        return User.from_dict(user_raw)

    def create_raw(self, user: User) -> requests.Response:
        return requests.post(
            url=f'{Config.url}/users',
            json=user.dict(),
        )
    
    def delete(self, token: str, id: int):
        response = self.delete_raw(token=token, id=id)

        if response.status_code != 204:
            pytest.fail(reason=f"сервeр ответил с ошибкой: {response.status_code}")


    def delete_raw(self, token: str, id: int) -> requests.Response:
        return requests.delete(
             url=f"{Config.url}/users/{id}",
             headers=auth_headers(token),
        )

    def update_role_raw(self, token: str, userId: int, role: str) -> requests.Response:
        return requests.patch(
            url=f'{Config.url}/users/{userId}/role/{role}',
            headers=auth_headers(token)
        )

    def update_role(self, token: str, userId: int, role: str):
        response = self.update_role_raw(token=token, role=role, userId=userId)

        if response.status_code != 200:
            pytest.fail(reason=f'Сервер ответил ошибкой {response.status_code}')

        return response.json()['msg']


