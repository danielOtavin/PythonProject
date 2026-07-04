import pytest
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

import browsers
from browsers import ChromeManager, FirefoxManager, EdgeManager
from config import Config
from pages.admin_page import AdminPage
from pages.base_page import BasePage
from pages.companies_page import CompanyPage
from pages.employees_page import EmployeePage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.signup_page import SignupPage
from pages.sql_page import SQLPage
from tests.conftest import user_token, admin_token


@pytest.fixture(scope='function', params=[ChromeManager, FirefoxManager, EdgeManager])
def browser(request) -> WebDriver:
    manager = request.param()
    browser = manager.get_driver()
    browser.maximize_window()
    yield browser
    browser.quit()


@pytest.fixture(scope='function', params=[admin_token, user_token])
def authorization(browser, admin_token, request) -> HomePage:
    browser.get(Config.url)
    browser.execute_script(f"window.localStorage.setItem('authToken', '{request.params}');")
    browser.open(HomePage.PATH)
    return HomePage(browser)


@pytest.fixture(scope='function')
def login_page(browser) -> LoginPage:
    login_page = LoginPage(browser)
    login_page.open()
    return LoginPage(browser)


@pytest.fixture(scope='function')
def signup_page(browser) -> SignupPage:
    signup_page = SignupPage(browser)
    signup_page.open()
    return SignupPage(browser)


@pytest.fixture(scope='function', params=[AdminPage, EmployeePage, CompanyPage, SQLPage])
def pages_admin_token(request, browser, admin_token):
    page = request.param(browser)
    page.open()
    browser.execute_script(f"window.localStorage.setItem('authToken', '{admin_token}');")
    browser.refresh()
    return page


@pytest.fixture(scope='function', params=[EmployeePage, CompanyPage, SQLPage])
def pages_user_token(request, browser, user_token):
    page = request.param(browser)
    page.open()
    browser.execute_script(f"window.localStorage.setItem('authToken', '{user_token}');")
    browser.refresh()
    return page
