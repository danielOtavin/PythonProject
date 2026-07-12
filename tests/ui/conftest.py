import sqlite3

import pytest
from selenium.webdriver.ie.webdriver import WebDriver

from browsers import ChromeManager, FirefoxManager, EdgeManager
from pages.admin_page import AdminPage
from pages.base_page import BasePage
from pages.companies_page import CompanyPage
from pages.employees_page import EmployeePage
from pages.home_page import HomePage
from pages.login_page_ import LoginPage
from pages.signup_page import SignupPage
from pages.sql_page import SQLPage


@pytest.fixture(scope='session', params=[ChromeManager, FirefoxManager, EdgeManager])
def browser(request) -> WebDriver:
    manager = request.param()
    browser = manager.get_driver()
    browser.maximize_window()
    yield browser
    browser.quit()


@pytest.fixture(scope='function', params=['admin_token', 'user_token'])
def authorization(browser, request, admin_token, user_token) -> HomePage:
    token_name = request.param
    token = request.getfixturevalue(token_name)
    home_page = HomePage(browser)
    browser.get(BasePage.BASE_URL)
    browser.execute_script(f"window.localStorage.setItem('authToken', '{token}');")
    home_page.open()
    return home_page


@pytest.fixture(scope='function')
def login_page(browser) -> LoginPage:
    login_page = LoginPage(browser)
    login_page.open()
    return login_page

@pytest.fixture(scope='function')
def signup_page(browser) -> SignupPage:
    signup_page = SignupPage(browser)
    signup_page.open()
    return signup_page


@pytest.fixture(scope='function', params=[AdminPage, EmployeePage, CompanyPage, SQLPage])
def pages_admin_token(request, browser, admin_token) -> AdminPage|EmployeePage|CompanyPage|SQLPage:
    browser.get(BasePage.BASE_URL)
    browser.execute_script(f"window.localStorage.setItem('authToken', '{admin_token}');")
    page = request.param(browser)
    page.open()
    yield page

    
@pytest.fixture(scope='function')
def page_specific_admin_token(browser, admin_token):
    def open_page(page_name: Literal['AdminPage', 'EmployeePage', 'CompanyPage', 'SQLPage']) -> AdminPage|EmployeePage|CompanyPage|SQLPage:
        pages_dict = {'AdminPage': AdminPage,
                      'EmployeePage': EmployeePage,
                      'CompanyPage': CompanyPage,
                      'SQLPage': SQLPage}
        if page_name not in pages_dict:
            raise ValueError(f'Страницы {page_name} не существует')
        selected_page = pages_dict[page_name]
        browser.get(BasePage.BASE_URL)
        browser.execute_script(f"window.localStorage.setItem('authToken', '{admin_token}');")
        page = selected_page(browser)
        page.open()
        return page
    return open_page


@pytest.fixture(scope='function', params=[EmployeePage, CompanyPage, SQLPage])
def pages_user_token(request, browser, user_token) -> EmployeePage|CompanyPage|SQLPage:
    browser.get(BasePage.BASE_URL)
    browser.execute_script(f"window.localStorage.setItem('authToken', '{user_token}');")
    page = request.param(browser)
    page.open()
    yield page

@pytest.fixture(scope='function')
def page_specific_user_token(browser, user_token):
    def open_page(page_name: Literal['EmployeePage','CompanyPage','SQLPage']) -> EmployeePage|CompanyPage|SQLPage:
        pages_dict = {'EmployeePage': EmployeePage,
                      'CompanyPage': CompanyPage,
                      'SQLPage': SQLPage}
        if page_name not in pages_dict:
            raise ValueError(f'Страницы {page_name} не существует')
        selected_page = pages_dict[page_name]
        browser.get(BasePage.BASE_URL)
        browser.execute_script(f"window.localStorage.setItem('authToken', '{user_token}');")
        page = selected_page(browser)
        page.open()
        return page
    return open_page


@pytest.fixture(scope='function')
def delete_user_from_db():
    def _delete(username):
        conn = sqlite3.connect('course.db')
        cursor = conn.cursor()
        cursor.execute('DELETE * FROM user WHERE login = ?', (username,))
        cursor.fetchall()
        conn.close()
    return _delete

@pytest.fixture(scope='function')
def clean_db():
    yield
    conn = sqlite3.connect('course.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user WHERE login != 'admin'")
    conn.commit()
    conn.close()
