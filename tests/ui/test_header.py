import pytest

from models.users import ADMIN, TEST
from pages.admin_page import AdminPage
from pages.companies_page import CompanyPage
from pages.employees_page import EmployeePage
from pages.sql_page import SQLPage


class TestHeader:
    @pytest.mark.parametrize('pages', [AdminPage, EmployeePage, CompanyPage, SQLPage])
    def test_admin_token_header_pages(self, pages_admin_token, pages):
        page = pages_admin_token(pages)
        assert ADMIN.login in page.header.get_user_info()
        page.header.click_home()
        page.wait_until_url_contains('/ui/home')
        page.header.click_quit()
        page.wait_until_url_contains('/ui/login')


    def test_user_token_header_pages(self, pages_user_token):
        page = pages_user_token
        assert TEST.login in page.header.get_user_info()
        page.header.click_home()
        page.wait_until_url_contains('/ui/home')
        page.header.click_quit()
        page.wait_until_url_contains('/ui/login')
