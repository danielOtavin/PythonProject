import pytest

from browsers import ChromeManager, FirefoxManager, EdgeManager
from pages.admin_page import AdminPage
from pages.companies_page import CompanyPage
from pages.employees_page import EmployeePage
from pages.home_page import HomePage
from pages.sql_page import SQLPage
from tests.conftest import user_token


@pytest.fixture(scope='function', params=[ChromeManager, FirefoxManager, EdgeManager])
def browser(request):
    manager = request.param()
    browser = manager.get_driver()
    browser.maximize_window()
    yield browser
    browser.quit()


@pytest.fixture(scope='function')
def admin_authorization(browser, admin_token) -> HomePage:
    browser.get('http://127.0.0.1:8010/ui/login')
    browser.execute_script(f"window.localStorage.setItem('authToken', '{admin_token}');")
    browser.refresh()
    return HomePage(browser)


@pytest.fixture(scope='function')
def user_authorization(browser, user_token) -> HomePage:
    browser.get('http://127.0.0.1:8010/ui/login')
    browser.execute_script(f"window.localStorage.setItem('authToken', '{user_token}');")
    browser.refresh()
    return HomePage(browser)


@pytest.fixture(scope='function')
def admin_page(browser, admin_token) -> AdminPage:
    browser.get('http://127.0.0.1:8010/ui/login')
    browser.execute_script(f"window.localStorage.setItem('authToken', '{admin_token}');")
    browser.refresh()
    return AdminPage(browser)


@pytest.fixture(scope='function', params=[admin_token, user_token])
def employees_page(browser, request) -> EmployeePage:
    browser.get('http://127.0.0.1:8010/ui/employees')
    browser.execute_script(f"window.localStorage.setItem('authToken', '{request.param}');")
    browser.refresh()
    return EmployeePage(browser)


@pytest.fixture(scope='function', params=[admin_token, user_token])
def companies_page(browser, request) -> CompanyPage:
    browser.get('http://127.0.0.1:8010/ui/companies')
    browser.execute_script(f"window.localStorage.setItem('authToken', '{request.param}');")
    browser.refresh()
    return CompanyPage(browser)


@pytest.fixture(scope='function', params=[admin_token, user_token])
def sql_page(browser, request) -> SQLPage:
    browser.get('http://127.0.0.1:8010/ui/sql')
    browser.execute_script(f"window.localStorage.setItem('authToken', '{request.param}');")
    browser.refresh()
    return SQLPage(browser)
