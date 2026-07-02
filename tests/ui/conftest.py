import pytest

from browsers import ChromeManager, FirefoxManager, EdgeManager
from config import Config
from pages.admin_page import AdminPage
from pages.companies_page import CompanyPage
from pages.employees_page import EmployeePage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.signup_page import SignupPage
from pages.sql_page import SQLPage
from tests.conftest import user_token, admin_token


@pytest.fixture(scope='function', params=[ChromeManager, FirefoxManager, EdgeManager])
def browser(request):
    manager = request.param()
    browser = manager.get_driver()
    browser.maximize_window()
    yield browser
    browser.quit()


@pytest.fixture(scope='function')
def admin_authorization(browser, admin_token) -> HomePage:
    browser.get(Config.url)
    browser.execute_script(f"window.localStorage.setItem('authToken', '{admin_token}');")
    browser.get(f'{Config.url}/ui/home')
    return HomePage(browser)


@pytest.fixture(scope='function')
def user_authorization(browser, user_token) -> HomePage:
    browser.get(Config.url)
    browser.execute_script(f"window.localStorage.setItem('authToken', '{user_token}');")
    browser.get(f'{Config.url}/ui/home')
    return HomePage(browser)


@pytest.fixture(scope='function')
def login_page(browser) -> LoginPage:
    browser.get(f'{Config.url}/ui/login')
    return LoginPage(browser)


@pytest.fixture(scope='function')
def signup_page(browser) -> SignupPage:
    browser.get(f'{Config.url}/ui/user/signup')
    return SignupPage(browser)


@pytest.fixture(scope='function')
def admin_page(browser, admin_token) -> AdminPage:
    browser.get(Config.url)
    browser.execute_script(f"window.localStorage.setItem('authToken', '{admin_token}');")
    browser.get(f'{Config.url}/ui/admin')
    return AdminPage(browser)


@pytest.fixture(scope='function', params=[admin_token, user_token])
def employees_page(browser, request) -> EmployeePage:
    browser.get(Config.url)
    browser.execute_script(f"window.localStorage.setItem('authToken', '{request.param}');")
    browser.get(f'{Config.url}/ui/employees')
    return EmployeePage(browser)


@pytest.fixture(scope='function', params=[admin_token, user_token])
def companies_page(browser, request) -> CompanyPage:
    browser.get(Config.url)
    browser.execute_script(f"window.localStorage.setItem('authToken', '{request.param}');")
    browser.get(f'{Config.url}/ui/companies')
    return CompanyPage(browser)


@pytest.fixture(scope='function', params=[admin_token, user_token])
def sql_page(browser, request) -> SQLPage:
    browser.get(Config.url)
    browser.execute_script(f"window.localStorage.setItem('authToken', '{request.param}');")
    browser.get(f'{Config.url}/ui/sql')
    return SQLPage(browser)