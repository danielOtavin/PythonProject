import pytest
import requests

from config import Config
from users import User
from api.base import auth_headers


class UserAPI:
    def create(self, user: User, token: str) -> User:
        response = self.create_raw(user=user, token=token)
        
        if response.status_code != 201:
            pytest.fail(reason=f"сервeр ответил с ошибкой: {response.status_code}")
            
        if not (user_raw := response.json()):
            pytest.fail(reason="не пришёл ответ")

        return User.model_validate(user_raw)

    def create_raw(self, user: User, token: str) -> requests.Response:
        return requests.post(
            url=f'{Config.url}/users',
            headers=auth_headers(token),
            json=user.model_dump(),
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

    def update_password_raw(self, userId: int, token: str, new_password: str) -> requests.Response:
        return requests.put(
            url=f'{Config.url}/users/{userId}/password',
            headers=auth_headers(token),
            json={'password': new_password})

    def update_password(self, userId: int, token: str, new_password: str):
        response = self.update_password_raw(userId = userId, token=token, new_password=new_password)

        if response.status_code != 200:
            pytest.fail(reason=f'Сервер ответил ошибкой {response.status_code}')
        return response.json()['msg']

