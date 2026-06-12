import pytest
import requests

from api.base import auth_headers
from companies import Company
from config import Config


class CompanyAPI:
    def create_raw(self, token: str, company: Company | dict) -> requests.Response:
        if isinstance(company, Company):
            payload = company.model_dump()
        elif isinstance(company, dict):
            payload = company
        else:
            raise TypeError(f"company должен быть Employee или dict, получен {type(company)}")
        return requests.post(f'{Config.url}/companies',
                             headers=auth_headers(token),
                             json=payload)


    def create(self, token: str, company: Company) -> Company:
        response = self.create_raw(token, company)

        if response.status_code != 201:
            pytest.fail(reason=f"Сервeр ответил с ошибкой: {response.status_code}")

        if not (company_raw := response.json()):
            pytest.fail(reason="Не пришёл ответ")

        return Company.model_validate(company_raw)


    def get_all_companies_raw(self, token: str, limit: int):
        return requests.get(f'{Config.url}/companies/all',
                            headers=auth_headers(token),
                            params={"limit": limit}
                            )


    def get_all_companies(self, token: str, limit: int):
        response = self.get_all_companies_raw(token, limit)

        if response.status_code != 200:
            pytest.fail(reason=f"Сервeр ответил с ошибкой: {response.status_code}")

        companies_data = response.json()

        if not companies_data:
            pytest.fail(reason="не пришёл ответ")

        return [Company.model_validate(comp) for comp in companies_data]


    def get_company_raw(self, token: str, companyId: int) -> requests.Response:
        return requests.get(f'{Config.url}/companies/{companyId}',
                            headers=auth_headers(token),
                            )

    def get_company(self, token: str, companyId: int) -> Company:
        response = self.get_company_raw(token, companyId)

        if response.status_code != 200:
            pytest.fail(reason=f"Сервeр ответил с ошибкой: {response.status_code}")

        if not (company_raw := response.json()):
            pytest.fail(reason="Не пришёл ответ")

        return Company.model_validate(company_raw)


    def update_company_raw(self, token: str, companyId: int, company: Company | dict) -> requests.Response:
        if isinstance(company, Company):
            payload = company.model_dump()
        elif isinstance(company, dict):
            payload = company
        else:
            raise TypeError(f"company должен быть Employee или dict, получен {type(company)}")
        return requests.put(f'{Config.url}/companies/{companyId}',
                            headers=auth_headers(token),
                            json=payload)

    def update_company(self, token: str, companyId: int, company: Company) -> Company:
        response = self.update_company_raw(token, companyId, company)

        if response.status_code != 200:
            pytest.fail(reason=f"Сервeр ответил с ошибкой: {response.status_code}")

        if not (company_raw := response.json()):
            pytest.fail(reason="Не пришёл ответ")

        return Company.model_validate(company_raw)

    def delete_company_raw(self, token: str, companyId: int) -> requests.Response:
        return requests.delete(f'{Config.url}/companies/{companyId}',
                               headers=auth_headers(token)
                               )

    def delete_company(self, token: str, companyId: int):
        response = self.delete_company_raw(token, companyId)

        if response.status_code != 204:
            pytest.fail(reason=f"Сервeр ответил с ошибкой: {response.status_code}")
