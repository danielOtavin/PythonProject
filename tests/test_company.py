import pytest
from companies import Company


class TestCompany:
    def test_create_company(self, company_api, admin_token, random_company):
        response = company_api.create_raw(admin_token, random_company)
        assert response.status_code == 201

    def test_get_company_by_id(self, company_api, admin_token, random_company):
        response = company_api.get_company_raw(admin_token, random_company.id)
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == random_company.id
        assert data['name'] == random_company.name
        assert data['year'] == random_company.year
        assert data['country'] == random_company.country

    def test_get_list_of_companies(self, company_api, admin_token, random_company):
        response = company_api.get_all_companies_raw(admin_token, limit=10)
        assert response.status_code == 200
        list_companies = response.json()
        assert isinstance(list_companies, list)
        assert len(list_companies) == 10

    def test_update_company(self, company_api, admin_token, random_company):
        payload = Company.random_company()
        response = company_api.update_company_raw(admin_token, random_company.id, payload)
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == random_company.id
        assert (data['name'] != random_company.name or
                data['year'] != random_company.year or
                data['country'] != random_company.country)

    def test_delete_company(self, company_api, admin_token, random_company):
        response = company_api.delete_company_raw(admin_token, random_company.id)
        assert response.status_code == 204
        response = company_api.get_company_raw(admin_token, random_company.id)
        assert response.status_code == 404
        response = company_api.delete_company_raw(admin_token, random_company.id)
        assert response.status_code == 404

    @pytest.mark.parametrize('company_data', [
        (lambda cmp: Company(name='', year=cmp.year, country=cmp.country)),
        (lambda cmp: Company(name=cmp.name, year=-2020, country=cmp.country)),
        (lambda cmp: Company(name=cmp.name, year='две тысячи', country=cmp.country)),
        (lambda cmp: Company(name=cmp.name, year=20000000, country=cmp.country)),
        (lambda cmp: {}),
        (lambda cmp: Company(name=cmp.name, year=cmp.year, country=cmp.country, work = True)),
    ], ids = ['Пустое имя компании',
              'Отрицательное значение года',
              'Неправильный тип данных',
              'Слишком большой год',
              'Пустые данные',
              'Лишнее поле'
    ])
    def test_create_company_negative(self, company_api, admin_token, random_company, company_data):
        payload = company_data(random_company)
        response = company_api.create_raw(admin_token, payload)
        assert response.status_code == 400


    @pytest.mark.parametrize('comp_id, expected_status_code', [
        (99999999999, 404),
        (0, 404),
        (-1, 404),
        ('один', 404)
    ], ids = ['Несуществующий id',
              'id равен нулю',
              'Отрицательный id',
              'Неправильный тип данных'
    ])
    def test_get_company_negative(self, company_api, admin_token, random_company, comp_id, expected_status_code):
        response = company_api.get_company_raw(admin_token, comp_id)
        assert response.status_code == expected_status_code

    @pytest.mark.parametrize('data, expected_status_code', [
        (lambda cmp: Company(name=cmp.name, year=-cmp.year, country=cmp.country), 400),
        (lambda cmp: Company(name=cmp.name, year=20000000, country=cmp.country), 400),
        (lambda cmp: Company(name=cmp.name, year=0, country=cmp.country), 400),
        (lambda cmp: Company(name=cmp.name, year='сто', country=cmp.country), 400),
        (lambda cmp: Company(name=cmp.name, year=cmp.year, country=cmp.country, work=True), 400),
        (lambda cmp: {}, 400)
    ], ids=['Отрицательное значение года',
            'Слишком большой год',
            'Год равен нулю',
            'Неправильный тип данных',
            'Лишнее поле',
            'Пустые данные'
    ])
    def test_update_company_negative(self, company_api, admin_token, random_company, data, expected_status_code):
        payload = data(random_company)
        response = company_api.update_company_raw(admin_token, random_company.id, payload)
        assert response.status_code == expected_status_code

    def test_delete_company_without_access(self, company_api, user_token, random_company):
        response = company_api.delete_company_raw(user_token, random_company.id)
        assert response.status_code == 403

    def test_delete_company_without_token(self, company_api, admin_token, random_company):
        response = company_api.delete_company_raw('', random_company.id)
        assert response.status_code == 401