import pytest

from models.companies import Company
from models.users import ADMIN
from pages.companies_page import CompanyPage


class TestCompaniesPage:
    # def test_delete_employee_via_company(self, clean_table_db, employee_api, admin_token, structure_api, company_api, browser,
    #                   pages_admin_token, db_check_obj):
    #     clean_table_db('employee')
    #     clean_table_db('company')
    #     employee = employee_api.create_employee(admin_token, Employee.random_employee())
    #     company = company_api.create_company(admin_token, Company.random_company())
    #     structure_api.add_employee_to_company_raw(company.id, admin_token, employee.id)
    #     companies_page = pages_admin_token(CompanyPage)
    #     companies_page.wait_until_visible(companies_page.get_company_item(company.id))
    #     companies_page.delete_employee_from_company_via_view_window(company.id, employee.id)
    #     assert db_check_obj('employee', employee.name) == []

    @pytest.mark.parametrize('open_page', [(CompanyPage, ADMIN)], indirect=True)
    def test_update_company_info(self, clean_table_db, admin_token, company_api, db_check_obj,
                                 open_page: CompanyPage):
        clean_table_db('employee')
        clean_table_db('company')
        company = company_api.create_company(admin_token, Company.random_company())
        company_data_upd = Company.random_company()
        open_page.page_refresh()
        open_page.wait_until_visible(open_page.get_company_item(company.id))
        open_page.update_company_data(company.id, company_data_upd)
        assert db_check_obj('company', company_data_upd.name) != []

    @pytest.mark.parametrize('open_page', [(CompanyPage, ADMIN)], indirect=True)
    def test_delete_company_info(self, clean_table_db, admin_token, company_api, db_check_obj, browser,
                                 open_page: CompanyPage):
        clean_table_db('employee')
        clean_table_db('company')
        company = company_api.create_company(admin_token, Company.random_company())
        open_page.page_refresh()
        open_page.wait_until_visible(open_page.get_company_item(company.id))
        open_page.delete_company_data(company.id)
        assert db_check_obj('company', company.id) == []


