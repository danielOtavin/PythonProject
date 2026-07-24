import sqlite3

import pytest

from models.companies import Company
from models.employees import Employee
from pages.companies_page import CompanyPage
from tests.conftest import admin_token, company_api, employee_api


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

    def test_update_company_info(self, clean_table_db, admin_token, company_api, db_check_obj, browser,
                                 pages_admin_token):
        clean_table_db('employee')
        clean_table_db('company')
        company = company_api.create_company(admin_token, Company.random_company())
        company_data_upd = Company.random_company()
        company_page = pages_admin_token(CompanyPage)
        company_page.wait_until_visible(company_page.get_company_item(company.id))
        company_page.update_company_data(company.id, company_data_upd)
        assert db_check_obj('company', company_data_upd.name) != []

    def test_delete_company_info(self, clean_table_db, admin_token, company_api, db_check_obj, browser,
                                 pages_admin_token):
        clean_table_db('employee')
        clean_table_db('company')
        company = company_api.create_company(admin_token, Company.random_company())
        company_page = pages_admin_token(CompanyPage)
        company_page.wait_until_visible(company_page.get_company_item(company.id))
        company_page.delete_company_data(company.id)
        assert db_check_obj('company', company.id) == []


