from typing import Optional
import requests

BASE_URL = 'http://127.0.0.1:8010'


class Token:
    def get_token(self, login, password):
        response = requests.post(BASE_URL + '/token',
                                 json= {'login': login,
                                        'password': password})
        if response.status_code == 200:
            token = response.json().get('token')
            headers = {'Authorization': f'Bearer {token}'}
            return headers
        return None

class Employee:
    name: str
    salary: int
    work: bool
    def __init__(self, headers: dict):
        self.headers = headers

    def create_employee(self, employee_data) -> Optional[dict]:
        """Создание работника"""
        response = requests.post(BASE_URL + '/employees',
                                 headers= self.headers,
                                 json= employee_data)
        if response.status_code == 201:
            print(f'Создан пользователь: {response.json()}')
            return response.json()
        else:
            print(f'Ошибка! Статус код: {response.status_code}, {response.text}')
            return None

    def get_all_employees(self, limit):
        """Получить информацию о всех работниках"""
        response = requests.get(BASE_URL + '/employees/all',
                                headers=self.headers,
                                params={'limit': limit})
        if response.status_code == 200:
            employees = response.json()
            for i, employee in enumerate(employees, start=1):
                print(f"{i}. {employee['name']} - {employee['salary']}")
            return employees
        else:
            print(f'Ошибка! Статус код: {response.status_code}, {response.text}')
            return None

    def get_single_employee(self, employeeId):
        """Получить информацию о работнике через его ID"""
        response = requests.get(BASE_URL + f'/employees/{employeeId}',
                                headers=self.headers)
        if response.status_code == 200:
            result = response.json()
            print(result)
            return result
        else:
            print(f'Ошибка! Статус код: {response.status_code}, {response.text}')
            return None

    def update_employee(self, employeeId, update_data):
        """Изменить информацию о работнике"""
        response = requests.put(BASE_URL + f'/employees/{employeeId}',
                                headers=self.headers,
                                json= update_data)
        if response.status_code == 200:
            result = response.json()
            print(f'Даннык пользователя {employeeId} обновлены. Новые данные: {result}')
            return result
        else:
            print(f'Ошибка! Статус код: {response.status_code}, {response.text}')
            return None

    def remove_employee(self, employeeId):
        """Удалить работника"""
        response = requests.delete(BASE_URL + f'/employees/{employeeId}',
                                   headers=self.headers)
        if response.status_code == 204:
            print(f"Пользователь {employeeId} удален")
            return True
        else:
            print(f"Ошибка {response.status_code}: {response.text}")
            return False

class Company:
    def __init__(self, headers: dict):
        self.headers = headers

    def create_company(self, company_data: dict):
        """Создать компанию"""
        response = requests.post(BASE_URL + '/companies',
                                 headers=self.headers,
                                 json=company_data)
        if response.status_code == 201:
            result = response.json()
            print(result)
            return result
        else:
            print(f'Ошибка! Статус код: {response.status_code}, {response.text}')
            return None

    def get_all_companies(self, limit):
        """Получить список всех компании"""
        response = requests.get(BASE_URL + '/companies/all',
                                headers=self.headers,
                                params={'limit': limit})
        if response.status_code == 200:
            companies = response.json()
            print("Список компаний:")
            for i, comp in enumerate(companies, start=1):
                print(f"{i}. {comp['name']} ({comp['country']}) - {comp['year']}")
            return companies
        else:
            print(f'Ошибка! Статус код: {response.status_code}, {response.text}')
            return None

    def get_company(self, companyId):
        """Получить компанию по ее ID"""
        response = requests.get(BASE_URL + f'/companies/{companyId}',
                                headers = self.headers)
        if response.status_code == 200:
            result = response.json()
            print(result)
            return result
        else:
            print(f'Ошибка! Статус код: {response.status_code}, {response.text}')
            return None

    def update_company(self, companyId, update_company_data):
        """Обновить инофрмацию о компании"""
        response = requests.put(BASE_URL + f'/companies/{companyId}',
                                headers=self.headers,
                                json= update_company_data)
        if response.status_code == 200:
            result = response.json()
            print(f'Даннык компании {companyId} обновлены. Новые данные: {result}')
            return result
        else:
            print(f'Ошибка! Статус код: {response.status_code}, {response.text}')
            return None

    def remove_company(self, companyId) -> bool:
        """Удалить компанию"""
        response = requests.delete(BASE_URL + f'/companies/{companyId}',
                                   headers=self.headers)
        if response.status_code == 204:
            print(f"Компания {companyId} удалена")
            return True
        else:
            print(f'Ошибка! Статус код: {response.status_code}, {response.text}')
            return False

class User:
    def __init__(self, headers: dict):
        self.headers = headers

    def create_user(self, login: str, password: str):
        """Создать нового пользователя"""
        response = requests.post(BASE_URL + '/users',
                                 headers=self.headers,
                                 json={'login': login,
                                       'password': password})
        if response.status_code == 201:
            result = response.json()
            print(f"Пользователь {result['id']} успешно создан")
            return result
        else:
            print(f"Ошибка {response.status_code}: {response.text}")
            print(f'Ошибка! Статус код: {response.status_code}, {response.text}')
            return None

    def update_user_role(self, userId, role) -> Optional[dict | bool]:
        """Обновить роль пользователя"""
        response = requests.patch(BASE_URL + f'/users/{userId}/roles/{role}',
                                  headers=self.headers)
        if response.status_code == 200 and role in ['read', 'write', 'admin']:
            result = response.json()
            print(f'Роль пользователя {userId} успешно изменена на {role}')
            return result
        elif response.status_code == 200 and role not in ['read', 'write', 'admin']:
            print('Указана неверная роль пользователя')
            return False
        else:
            print(f'Ошибка! Статус код: {response.status_code}, {response.text}')
            return None

    def update_user_password(self, userId) -> Optional[dict | bool]:
        """Обновить пароль пользователя"""
        data = {'password': 'admin'}
        response = requests.patch(BASE_URL + f'/users/{userId}/password',
                                  headers=self.headers,
                                  json=data)
        if response.status_code == 200:
            result = response.json()
            print(f'Пароль пользователя {userId} изменен на {data["password"]}')
            return result
        else:
            print(f'Ошибка! Статус код: {response.status_code}, {response.text}')
            return None

    def delete_user(self, userId) -> bool:
        """Удалить пользователя"""
        response = requests.delete(BASE_URL + f'/users/{userId}',
                                   headers=self.headers)
        if response.status_code == 204:
            return True
        else:
            print(f'Ошибка! Статус код: {response.status_code}, {response.text}')
            return False

class Structure:
    def __init__(self, headers: dict):
        self.headers = headers

    def get_company_employees(self, companyId: int) -> Optional[dict]:
        """Получить сотрудников компании"""
        response = requests.get(BASE_URL + f'/structure/{companyId}',
                                headers=self.headers)
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            print(f'Ошибка! Статус код: {response.status_code}, {response.text}')
            return None

    def add_employees_to_company(self, companyId: int, employeeId: list) -> Optional[dict]:
        """Добавить сотрудников в компанию"""
        response = requests.post(BASE_URL + f'/structure/{companyId}',
                                 headers=self.headers,
                                 json= employeeId)
        if response.status_code == 200:
            result = response.json()
            print(f'Сотрудники {employeeId} добавлены в компанию {result}')
            return result
        else:
            print(f'Ошибка! Статус код: {response.status_code}, {response.text}')
            return None

    def delete_employees_from_company(self, companyId: int, employeeId: list) -> bool:
        """Удалить сотрудников из компании"""
        response = requests.delete(BASE_URL + f'/structure/{companyId}',
                                   headers=self.headers,
                                   json=employeeId)
        if response.status_code == 204:
            print('	Сотрудники удалены')
            return True
        else:
            print(f'Ошибка! Статус код: {response.status_code}, {response.text}')
            return False

token = Token()
a = token.get_token('admin', 'admin')
employee = Employee(a)
employee.create_employee({'name': 'Иван', 'salary': 500, 'work': True})