from typing import Optional
import requests
import faker

BASE_URL = 'http://127.0.0.1:8010'

def get_token() -> str:
    """Создание токена авторизации"""
    response = requests.post(BASE_URL + '/token', json={'login': 'admin', 'password': 'admin'})
    return response.json()['token']

class Employee:
    def __init__(self, token: str):
        self.token = token
        self.headers = {'Authorization': f'Bearer {token}'}
        self.fake = faker.Faker('ru_RU')

    def create_employee(self) -> Optional[int]:
        """Создание работника"""
        response = requests.post(BASE_URL + '/employees',
                                 headers = self.headers,
                                 json={'name': self.fake.name(),
                                       'salary': self.fake.random_int(100, 1000),
                                       'work': self.fake.boolean()})
        if response.status_code == 201:
            print(f'Создан пользователь: {response.json()}')
            return response.json()['id']
        else:
            print(f'Ошибка! Статус код: {response.status_code}, {response.text}')
            return None

    def get_all_employees(self):
        """Получить информацию о всех работниках"""
        response = requests.get(BASE_URL + '/employees/all',
                                headers=self.headers,
                                params={'limit': 10})
        if response.status_code == 200:
            employees = response.json()
            for i, emp in enumerate(employees, start=1):
                print(f"{i}. {emp['name']} - {emp['salary']}")
            return employees
        else:
            print(f'Ошибка! Статус код: {response.status_code}, {response.text}')
            return None

    def get_single_employee(self, employeeId):
        """Получить информацию о работнике через его ID"""
        response = requests.get(BASE_URL + f'/employees/{employeeId}', headers=self.headers)
        if response.status_code == 200:
            result = response.json()
            print(result)
            return result
        else:
            print(f'Ошибка! Статус код: {response.status_code}, {response.text}')
            return None

    def update_employee(self, employeeId):
        """Изменить информацию о работнике"""
        response = requests.put(BASE_URL + f'/employees/{employeeId}',
                                headers=self.headers,
                                json={'name': self.fake.name(),
                                      'salary': self.fake.random_int(500, 2000),
                                      'work': self.fake.boolean()})
        if response.status_code == 200:
            result = response.json()
            print(f'Даннык пользователя {employeeId} обновлены. Новые данные: {result}')
            return result
        else:
            print(f'Ошибка! Статус код: {response.status_code}, {response.text}')
            return None

    def remove_employee(self, employeeId):
        """Удалить работника"""
        response = requests.delete(BASE_URL + f'/employees/{employeeId}', headers=self.headers)
        if response.status_code == 204:
            print(f"Пользователь {employeeId} удален")
            return True
        else:
            print(f"Ошибка {response.status_code}: {response.text}")
            return False

class Company:
    def __init__(self, token: str):
        self.token = token
        self.headers = {'Authorization': f'Bearer {token}'}
        self.fake = faker.Faker('ru_RU')

    def create_company(self):
        """Создать компанию"""
        response = requests.post(BASE_URL + '/companies',
                                 headers=self.headers,
                                 json={'name': self.fake.company(),
                                       'year': self.fake.year(),
                                       'country': self.fake.country()})
        if response.status_code == 201:
            result = response.json()
            print(result)
            return result
        else:
            print(f"Ошибка {response.status_code}: {response.text}")
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
            print(f"Ошибка {response.status_code}: {response.text}")
            return None

    def get_company(self, companyId):
        """Получить компанию по ее ID"""
        response = requests.get(BASE_URL + f'/companies/{companyId}', headers = self.headers)
        if response.status_code == 200:
            result = response.json()
            print(result)
            return result
        else:
            print(f'Ошибка! Статус код: {response.status_code}, {response.text}')
            return None

    def update_company(self, companyId):
        """Обновить инофрмацию о компании"""
        response = requests.put(BASE_URL + f'/companies/{companyId}',
                                headers=self.headers,
                                json={'name': self.fake.country(),
                                      'year': self.fake.year(),
                                      'country': self.fake.country()})
        if response.status_code == 200:
            result = response.json()
            print(f'Даннык компании {companyId} обновлены. Новые данные: {result}')
            return result
        else:
            print(f'Ошибка! Статус код: {response.status_code}, {response.text}')
            return None

    def remove_company(self, companyId):
        """Удалить компанию"""
        response = requests.delete(BASE_URL + f'/companies/{companyId}', headers=self.headers)
        if response.status_code == 204:
            print(f"Компания {companyId} удалена")
            return True
        else:
            print(f"Ошибка {response.status_code}: {response.text}")
            return False

class User:
    def __init__(self, token: str):
        self.token = token
        self.headers = {'Authorization': f'Bearer {token}'}

    def update_user_password(self, userId):
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
            print(f"Ошибка {response.status_code}: {response.text}")
            return False

    def delete_user(self, userId):
        """Удалить пользователя"""
        response = requests.delete(BASE_URL + f'/users/{userId}', headers=self.headers)
        if response.status_code == 204:
            return True
        else:
            return False

    def update_user_role(self, userId, role):
        """Обновить роль пользователя"""
        response = requests.patch(BASE_URL + f'/users/{userId}/roles/{role}', headers=self.headers)
        if response.status_code == 200 and role in ['read', 'write', 'admin']:
            result = response.json()
            print(f'Роль пользователя {userId} успешно изменена на {role}')
            return result
        elif response.status_code == 200 and role not in ['read', 'write', 'admin']:
            print('Указана неверная роль пользователя')
            return False
        else:
            print(f"Ошибка {response.status_code}: {response.text}")
            return False

    def create_user(self, login: str, password: str):
        """Создать нового пользователя"""
        response = requests.post(BASE_URL + '/users', headers=self.headers, json={'login': login, 'password': password})
        if response.status_code == 201:
            print('Пользователь успешно создан')
            return response.json()['id']
        else:
            print(f"Ошибка {response.status_code}: {response.text}")
            return False

class Structure:
    def __init__(self, token: str):
        self.token = token
        self.headers = {'Authorization': f'Bearer {token}'}

    def get_company_employees(self, companyId):
        """Получить сотрудников компании"""
        response = requests.get(BASE_URL + f'/structure/{companyId}', headers=self.headers)
        if response.status_code == 200:
            result = response.json()
            print(f'Сотрудники компании {companyId}: {result["employees"]}')
            return result
        else:
            print(f"Ошибка {response.status_code}: {response.text}")
            return None

    def add_employees_to_company(self, companyId):
        """Добавить сотрудников в компанию"""
        response = requests.post(BASE_URL + f'/structure/{companyId}', headers=self.headers)
        if response.status_code == 200:
            result = response.json()
            print('Сотрудники добавлены в компанию')
            return result
        else:
            print(f"Ошибка {response.status_code}: {response.text}")
            return False

    def delete_employees_from_company(self, companyId):
        """Удалить сотрудников из компании"""
        response = requests.delete(BASE_URL + f'/structure/{companyId}', headers=self.headers)
        if response.status_code == 204:
            print('	Сотрудники удалены')
            return True
        else:
            print(f"Ошибка {response.status_code}: {response.text}")
            return False

