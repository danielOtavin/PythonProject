from http.client import HTTPException
from typing import Optional
import requests
import faker

BASE_URL = 'http://127.0.0.1:8010'


class Token:
    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password
        self.headers = None

    def get_token(self):
        response = requests.post(BASE_URL + '/token',
                                   json={'login': self.login,
                                         'password': self.password})
        token = response.json()['token']
        self.headers = {'Authorization': f'Bearer {token}'}
        return self.headers

class Employee:
    name: str
    salary: int
    work: bool

    def create_employee(self, employee_data, auth: Token) -> Optional[dict]:
        """Создание работника"""
        response = requests.post(BASE_URL + '/employees',
                                 headers = auth.get_token(),
                                 json= employee_data)
        if response.status_code == 201:
            print(f'Создан пользователь: {response.json()}')
            return response.json()
        else:
            print(f'Ошибка! Статус код: {response.status_code}, {response.text}')
            return None

    def get_all_employees(self, limit, auth: Token):
        """Получить информацию о всех работниках"""
        response = requests.get(BASE_URL + '/employees/all',
                                headers = auth.get_token(),
                                params={'limit': limit})
        if response.status_code == 200:
            employees = response.json()
            for i, employee in enumerate(employees, start=1):
                print(f"{i}. {employee['name']} - {employee['salary']}")
            return employees
        else:
            raise HTTPException(f'Ошибка! Статус код: {response.status_code}, {response.text}')

    def get_single_employee(self, employeeId, auth: Token):
        """Получить информацию о работнике через его ID"""
        response = requests.get(BASE_URL + f'/employees/{employeeId}',
                                headers=auth.get_token())
        if response.status_code == 200:
            result = response.json()
            print(result)
            return result
        else:
            raise HTTPException(f'Ошибка! Статус код: {response.status_code}, {response.text}')

    def update_employee(self, employeeId, update_data, auth: Token):
        """Изменить информацию о работнике"""
        response = requests.put(BASE_URL + f'/employees/{employeeId}',
                                headers=auth.get_token(),
                                json= update_data)
        if response.status_code == 200:
            result = response.json()
            print(f'Даннык пользователя {employeeId} обновлены. Новые данные: {result}')
            return result
        else:
            raise HTTPException(f'Ошибка! Статус код: {response.status_code}, {response.text}')

    def remove_employee(self, employeeId, auth: Token):
        """Удалить работника"""
        response = requests.delete(BASE_URL + f'/employees/{employeeId}',
                                   headers=auth.get_token())
        if response.status_code == 204:
            print(f"Пользователь {employeeId} удален")
            return True
        else:
            print(f"Ошибка {response.status_code}: {response.text}")
            return False

class Company:
    def create_company(self, company_data: dict, auth: Token):
        """Создать компанию"""
        response = requests.post(BASE_URL + '/companies',
                                 headers=auth.get_token(),
                                 json=company_data)
        if response.status_code == 201:
            result = response.json()
            print(result)
            return result
        else:
            raise HTTPException(f"Ошибка {response.status_code}: {response.text}")

    def get_all_companies(self, limit, auth: Token):
        """Получить список всех компании"""
        response = requests.get(BASE_URL + '/companies/all',
                                headers=auth.get_token(),
                                params={'limit': limit})
        if response.status_code == 200:
            companies = response.json()
            print("Список компаний:")
            for i, comp in enumerate(companies, start=1):
                print(f"{i}. {comp['name']} ({comp['country']}) - {comp['year']}")
            return companies
        else:
            raise HTTPException(f"Ошибка {response.status_code}: {response.text}")

    def get_company(self, companyId, auth: Token):
        """Получить компанию по ее ID"""
        response = requests.get(BASE_URL + f'/companies/{companyId}',
                                headers = auth.get_token())
        if response.status_code == 200:
            result = response.json()
            print(result)
            return result
        else:
            raise HTTPException(f"Ошибка {response.status_code}: {response.text}")

    def update_company(self, companyId, update_company_data, auth: Token):
        """Обновить инофрмацию о компании"""
        response = requests.put(BASE_URL + f'/companies/{companyId}',
                                headers=auth.get_token(),
                                json= update_company_data)
        if response.status_code == 200:
            result = response.json()
            print(f'Даннык компании {companyId} обновлены. Новые данные: {result}')
            return result
        else:
            raise HTTPException(f"Ошибка {response.status_code}: {response.text}")


    def remove_company(self, companyId, auth: Token) -> bool:
        """Удалить компанию"""
        response = requests.delete(BASE_URL + f'/companies/{companyId}',
                                   headers=auth.get_token())
        if response.status_code == 204:
            print(f"Компания {companyId} удалена")
            return True
        else:
            raise HTTPException(f"Ошибка {response.status_code}: {response.text}")


class User:
    def create_user(self, login: str, password: str, auth: Token):
        """Создать нового пользователя"""
        response = requests.post(BASE_URL + '/users',
                                 headers=auth.get_token(),
                                 json={'login': login,
                                       'password': password})
        if response.status_code == 201:
            result = response.json()
            print(f"Пользователь {result['id']} успешно создан")
            return result
        else:
            print(f"Ошибка {response.status_code}: {response.text}")
            raise HTTPException(f"Ошибка {response.status_code}: {response.text}")

    def update_user_role(self, userId, role, auth: Token) -> Optional[dict | bool]:
        """Обновить роль пользователя"""
        response = requests.patch(BASE_URL + f'/users/{userId}/roles/{role}',
                                  headers=auth.get_token())
        if response.status_code == 200 and role in ['read', 'write', 'admin']:
            result = response.json()
            print(f'Роль пользователя {userId} успешно изменена на {role}')
            return result
        elif response.status_code == 200 and role not in ['read', 'write', 'admin']:
            print('Указана неверная роль пользователя')
            return False
        else:
            raise HTTPException(f"Ошибка {response.status_code}: {response.text}")


    def update_user_password(self, userId, auth: Token) -> Optional[dict | bool]:
        """Обновить пароль пользователя"""
        data = {'password': 'admin'}
        response = requests.patch(BASE_URL + f'/users/{userId}/password',
                                  headers=auth.get_token(),
                                  json=data)
        if response.status_code == 200:
            result = response.json()
            print(f'Пароль пользователя {userId} изменен на {data["password"]}')
            return result
        else:
            print(f"Ошибка {response.status_code}: {response.text}")
            return False

    def delete_user(self, userId, auth: Token) -> bool:
        """Удалить пользователя"""
        response = requests.delete(BASE_URL + f'/users/{userId}',
                                   headers=auth.get_token())
        if response.status_code == 204:
            return True
        else:
            return False


class Structure:
    def get_company_employees(self, companyId: int, auth: Token) -> Optional[dict]:
        """Получить сотрудников компании"""
        response = requests.get(BASE_URL + f'/structure/{companyId}',
                                headers=auth.get_token())
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            raise HTTPException(f"Ошибка {response.status_code}: {response.text}")

    def add_employees_to_company(self, companyId: int, employeeId: list, auth: Token) -> Optional[dict]:
        """Добавить сотрудников в компанию"""
        response = requests.post(BASE_URL + f'/structure/{companyId}',
                                 headers=auth.get_token(),
                                 json= employeeId)
        if response.status_code == 200:
            result = response.json()
            print(f'Сотрудники {employeeId} добавлены в компанию {result}')
            return result
        else:
            raise HTTPException(f"Ошибка {response.status_code}: {response.text}")

    def delete_employees_from_company(self, companyId: int, employeeId: list, auth: Token) -> bool:
        """Удалить сотрудников из компании"""
        response = requests.delete(BASE_URL + f'/structure/{companyId}',
                                   headers=auth.get_token(),
                                   json=employeeId)
        if response.status_code == 204:
            print('	Сотрудники удалены')
            return True
        else:
            raise HTTPException(f"Ошибка {response.status_code}: {response.text}")

