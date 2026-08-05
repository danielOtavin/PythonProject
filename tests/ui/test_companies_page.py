import allure

from dbase.data_base import TableName
from models.companies import Company
from models.employees import Employee
from models.users import ADMIN
from pages.companies_page import CompanyPage
from pytest import mark

@mark.companies
class TestCompaniesPage:
    @mark.skip(reason='не работает')
    @mark.parametrize('open_page', [(CompanyPage, ADMIN)], indirect=True)
    def test_delete_employee_via_company(self, clean_companies_db, clean_employees_db, employee_api,
                                         admin_token, structure_api, company_api, browser, open_page: CompanyPage, db):
        employee = employee_api.create_employee(admin_token, Employee.random_employee())
        company = company_api.create_company(admin_token, Company.random_company())
        structure_api.add_employee_to_company_raw(company.id, admin_token, employee.id)
        open_page.page_refresh()
        open_page.wait_until_visible(open_page.get_company_item(company.id))
        open_page.delete_employee_from_company_via_view_window(company.id, employee.id)
        assert db.check_object_in_db(TableName.EMPLOYEE, employee.id) == []

    @mark.parametrize('open_page', [(CompanyPage, ADMIN)], indirect=True)
    def test_update_company_info(self, clean_companies_db, clean_employees_db, admin_token, company_api,
                                 open_page: CompanyPage, db):
        with allure.step('Создать компанию и данные для ее обновления'):
            company = company_api.create_company(admin_token, Company.random_company())
            company_data_upd = Company.random_company()
        with allure.step('Обновить данные компании'):
            open_page.page_refresh()
            open_page.wait_until_visible(open_page.get_company_item(company.id))
            open_page.update_company_data(company.id, company_data_upd)
            result_dict = {db.check_object_in_db(TableName.COMPANY, company.id)[0][1],
                           db.check_object_in_db(TableName.COMPANY, company.id)[0][2],
                           db.check_object_in_db(TableName.COMPANY, company.id)[0][3]}
            assert result_dict == {company_data_upd.name,
                                   company_data_upd.country,
                                   company_data_upd.year}


    @mark.parametrize('open_page', [(CompanyPage, ADMIN)], indirect=True)
    def test_delete_company_info(self, clean_employees_db, clean_companies_db, admin_token, company_api, db,
                                 open_page: CompanyPage):
        with allure.step('Создать компанию'):
            company = company_api.create_company(admin_token, Company.random_company())
        with allure.step('Удалить компанию и просмотреть данные компании после удаления в БД'):
            open_page.page_refresh()
            open_page.wait_until_visible(open_page.get_company_item(company.id))
            open_page.delete_company_data(company.id)
            assert db.check_object_in_db(TableName.COMPANY, company.id) == []


