import random

import allure
import pytest
from models.companies import Company

@allure.feature('API Компании')
class TestCompany:
    @allure.story('Позитивный сценарий CRUD операций')
    @allure.title('Тестирование CRUD операций для компании')
    def test_create_get_and_delete_company(self, company_api, admin_token):
        with allure.step('Создать данные для компании'):
            created_company_data = Company.random_company()
        with allure.step('Отправить запрос на создание компании'):
            response_create = company_api.create_company_raw(admin_token, created_company_data)
        with allure.step('Десериализировать ответ сервера'):
            data_create = response_create.json()
        with allure.step('Получить ID компании'):
            company_id = data_create.get('id')
        with allure.step('Проверить статус код ответа сервера'):
            assert response_create.status_code == 201
        with allure.step('Проверить ID компании больше и не равен нулю'):
            assert data_create.pop('id') > 0
        with allure.step('Проверить соответсвие данных созданной компании полученным данным'):
            assert data_create == {
                'name': created_company_data.name,
                'year': created_company_data.year,
                'country': created_company_data.country
            }
        with allure.step('Отправить запрос на получение компании'):
            response_get = company_api.get_company_raw(admin_token, company_id)
        with allure.step('Десериализировать ответ сервера'):
            data_get = response_get.json()
        with allure.step('Проверить статус код ответа сервера'):
            assert response_get.status_code == 200
        with allure.step('Проверить ID полученной компании больше и не равен нулю'):
            assert data_get.pop('id') > 0
        with allure.step('Проверить соответствие данных полученной компании ожидаемым данным'):
            assert data_get == {
                'name': created_company_data.name,
                'year': created_company_data.year,
                'country': created_company_data.country
            }
        with allure.step('Создать данные для обновления данных компании'):
            updated_company_data = Company.random_company()
        with allure.step('Отправить запрос на обновление данных компании'):
            response_update = company_api.update_company_raw(admin_token, company_id, updated_company_data)
        with allure.step('Проверить статус код ответа сервера'):
            assert response_update.status_code == 200
        with allure.step('Проверить соответствие полученного ID'):
            assert response_update.json().get('id') == company_id

        with allure.step('Отправить запрос на удаление компании'):
            response_delete = company_api.delete_company_raw(admin_token, company_id)
        with allure.step('Проверить статус код ответа сервера'):
            assert response_delete.status_code == 204
        with allure.step('Отправить запрос на получение данных удаленной компании'):
            get_deleted_company = company_api.get_company_raw(admin_token, company_id)
        with allure.step('Проверить статус код ответа сервера'):
            assert get_deleted_company.status_code == 400
        with allure.step('Отправить запрос на удаление компании'):
            second_delete = company_api.delete_company_raw(admin_token, company_id)
        with allure.step('Проверить статус код ответа сервера'):
            assert second_delete.status_code == 404

    @allure.story('Получение списка компаний')
    @allure.step('Тестирование успешного получения списка компаний')
    def test_get_list_of_companies(self, company_api, admin_token):
        with allure.step('Обозначить лимит поиска'):
            limit = random.randint(1,10)
        with allure.step('Отправить запрос на получение списка компаний'):
            response = company_api.get_all_companies_raw(admin_token, limit)
        with allure.step('Десереализовать ответ сервера'):
            list_companies = response.json()
        with allure.step('Проверить статус код ответа сервера'):
            assert response.status_code == 200
        with allure.step('Проверить соответсвие типа данных, полученных от сервера, типу list'):
            assert isinstance(list_companies, list)
        with allure.step('Проверить длина списка равна лимиту поиска'):
            assert len(list_companies) == limit

    @pytest.mark.parametrize('company_data', [
        (lambda cmp: Company(name='', year=cmp.year, country=cmp.country)),
        (lambda cmp: Company(name=cmp.name, year=-2020, country=cmp.country)),
        (lambda cmp: Company(name=cmp.name, year='2000', country=cmp.country)),
        (lambda cmp: Company(name=cmp.name, year=20000000, country=cmp.country)),
        (lambda cmp: {}),
        (lambda cmp: Company(name=cmp.name, year=cmp.year, country=cmp.country, work = True)),
    ], ids = ['empty_company_name_field',
              'negative_year_value',
              'unknown_data_type',
              'too_huge_year_value',
              'empty_data',
              'extra_field'
    ])
    @allure.story('Создание')
    @allure.step('Тестирование негативных сценариев создания компании')
    def test_create_company_negative(self, company_api, admin_token, random_company, company_data):
        with allure.step('Создать данные для компании'):
            payload = company_data(random_company)
        with allure.step('Отправить запрос на создание компании'):
            response = company_api.create_company_raw(admin_token, payload)
        with allure.step('Проверить статус код ответа сервера'):
            assert response.status_code == 400


    @pytest.mark.parametrize('comp_id, expected_status_code', [
        (99999999999, 404),
        (0, 404),
        (-1, 404),
        ('1', 404)
    ], ids = ['unknown_id',
              'id_is_null',
              'negative_id',
              'unknown_data_type'
    ])
    @allure.story('Получение данных компании')
    @allure.step('Тестирование негативного сценария получения данных компании')
    def test_get_company_negative(self, company_api, admin_token, random_company, comp_id, expected_status_code):
        with allure.step('Отправить запрос на получение компании'):
            response = company_api.get_company_raw(admin_token, comp_id)
        with allure.step('Проверить статус код ответа сервера'):
            assert response.status_code == expected_status_code

    @pytest.mark.parametrize('data, expected_status_code', [
        (lambda cmp: Company(name=cmp.name, year=-cmp.year, country=cmp.country), 400),
        (lambda cmp: Company(name=cmp.name, year=20000000, country=cmp.country), 400),
        (lambda cmp: Company(name=cmp.name, year=0, country=cmp.country), 400),
        (lambda cmp: Company(name=cmp.name, year='100', country=cmp.country), 400),
        (lambda cmp: Company(name=cmp.name, year=cmp.year, country=cmp.country, work=True), 400),
        (lambda cmp: {}, 400)
    ], ids=['negative_year_value',
            'too_huge_year_value',
            'year_value_is_null',
            'unknown_data_type',
            'extra_field',
            'empty_data'
    ])
    @allure.story('Обновление компани')
    @allure.step('Тестирование негативного сценария обновления данных компании')
    def test_update_company_negative(self, company_api, admin_token, random_company, data, expected_status_code):
        with allure.step('Создать данные для компании'):
            payload = data(Company.random_company())
        with allure.step('Отправить запрос на обновление данных компании'):
            response = company_api.update_company_raw(admin_token, random_company.id, payload)
        with allure.step('Проверить статус код ответа сервера'):
            assert response.status_code == expected_status_code


    @pytest.mark.parametrize('token, expected_status_code', [
        ('user_token', 403),
        ('empty_token', 401)
    ], ids=['user_token',
            'empty_token'])
    @allure.story('Удаление данных компани')
    @allure.step('Тестирование негативного сценария удаления компании')
    def test_delete_company(self, company_api, user_token, random_company, token, expected_status_code):
        tokens = {'user_token': user_token,
                  'empty_token': ''}
        used_token = tokens[token]
        with allure.step('Отправить запрос на удаление данных компании'):
            response = company_api.delete_company_raw(used_token, random_company.id)
        with allure.step('Проверить статус код ответа сервера'):
            assert response.status_code == expected_status_code
