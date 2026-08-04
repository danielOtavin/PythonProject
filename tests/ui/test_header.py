import pytest

from models.users import ADMIN, TEST
from pages.admin_page import AdminPage
from pages.companies_page import CompanyPage
from pages.employees_page import EmployeePage
from pages.sql_page import SQLPage


class TestHeader:
    @pytest.mark.parametrize('open_page', [(AdminPage, ADMIN),
                                           (EmployeePage, ADMIN),
                                           (CompanyPage, ADMIN),
                                           (SQLPage, ADMIN)], indirect=True)
    def test_admin_token_header_pages(self, open_page):
        assert ADMIN.login in open_page.get_user_info()
        open_page.click_home()
        open_page.wait_until_url_contains('/ui/home')
        open_page.click_quit()
        open_page.wait_until_url_contains('/ui/login')

    @pytest.mark.parametrize('open_page', [(AdminPage, TEST),
                                           (EmployeePage, TEST),
                                           (CompanyPage, TEST),
                                           (SQLPage, TEST)
                                           ], indirect=True)
    def test_user_token_header_pages(self, open_page):
        assert TEST.login in open_page.get_user_info()
        open_page.click_home()
        open_page.wait_until_url_contains('/ui/home')
        open_page.click_quit()
        open_page.wait_until_url_contains('/ui/login')

