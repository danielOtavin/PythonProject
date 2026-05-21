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