import pytest
from companies import Company


class TestCompany:
    def test_create_get_and_delete_company(self, company_api, admin_token):
        created_company_data = Company.random_company()
        response_create = company_api.create_company_raw(admin_token, created_company_data)
        data_create = response_create.json()
        company_id = data_create.get('id')
        assert response_create.status_code == 201
        assert data_create.pop('id') > 0
        assert data_create == {
            'name': created_company_data.name,
            'year': created_company_data.year,
            'country': created_company_data.country
        }

        response_get = company_api.get_company_raw(admin_token, company_id)
        data_get = response_get.json()
        assert response_get.status_code == 200
        assert data_get.pop('id') > 0
        assert data_get == {
            'name': created_company_data.name,
            'year': created_company_data.year,
            'country': created_company_data.country
        }
        response_delete = company_api.delete_company_raw(admin_token, company_id)
        assert response_delete.status_code == 204
        get_deleted_company = company_api.get_company_raw(admin_token, company_id)
        assert get_deleted_company.status_code == 400
        second_delete = company_api.delete_company_raw(admin_token, company_id)
        assert second_delete.status_code == 404

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
    def test_create_company_negative(self, company_api, admin_token, random_company, company_data):
        payload = company_data(random_company)
        response = company_api.create_company_raw(admin_token, payload)
        assert response.status_code == 400


    @pytest.mark.parametrize('comp_id, expected_status_code', [
        (99999999999, 404),
        (0, 404),
        (-1, 404),
        ('один', 404)
    ], ids = ['unknown_id',
              'id_is_null',
              'negative_id',
              'unknown_data_type'
    ])
    def test_get_company_negative(self, company_api, admin_token, random_company, comp_id, expected_status_code):
        response = company_api.get_company_raw(admin_token, comp_id)
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
    def test_update_company_negative(self, company_api, admin_token, random_company, data, expected_status_code):
        payload = data(random_company)
        response = company_api.update_company_raw(admin_token, random_company.id, payload)
        assert response.status_code == expected_status_code


    @pytest.mark.parametrize('expected_token, expected_status_code', [
        ('user_token', 403),
        ('empty_token', 401)
    ], ids=['user_token',
            'empty_token'])
    def test_delete_company(self, company_api, user_token, random_company, expected_token, expected_status_code):
        tokens = {'user_token': user_token,
                  'empty_token': ''}
        token = tokens[expected_token]
        response = company_api.delete_company_raw(token, random_company.id)
        assert response.status_code == expected_status_code
