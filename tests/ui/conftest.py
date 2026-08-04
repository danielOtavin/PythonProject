import sqlite3
from typing import Generator, Literal
from api.token import Token

import pytest

from browsers import ChromeManager, FirefoxManager, EdgeManager
from config import Config
from pages.base_page import BasePage
from pages.home_page import HomePage
from pages.login_page_ import LoginPage
from pages.signup_page import SignupPage


@pytest.fixture(scope='session', params=[ChromeManager, FirefoxManager, EdgeManager])
def browser(request) -> Generator[BasePage]:
    manager = request.param()
    browser = manager.get_driver()
    browser.maximize_window()
    yield browser
    browser.quit()

def local_storage_script(browser, token: str):
    return browser.execute_script(f"window.localStorage.setItem('authToken', '{token}');")

@pytest.fixture(scope='function', params=['admin_token', 'user_token'])
def authorization(browser, request, admin_token, user_token) -> HomePage:
    token_name = request.param
    token = request.getfixturevalue(token_name)
    home_page = HomePage(browser)
    browser.get(BasePage.BASE_URL)
    local_storage_script(browser, token)
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

@pytest.fixture(scope='function')
def home_page(browser, admin_token):
    browser.get(BasePage.BASE_URL)
    local_storage_script(browser, admin_token)
    page = HomePage(browser)
    page.open()
    return page

@pytest.fixture
def open_page(request, browser) -> Generator[BasePage]:
    page, user = request.param
    token = Token().get_token(user=user)
    ready_page = page(browser)
    ready_page.open()
    local_storage_script(browser, token)
    ready_page.open()
    yield ready_page
    local_storage_script(browser, 'null')

class DB:
    conn: sqlite3.Connection
    cursor: sqlite3.Cursor

    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

@pytest.fixture(scope='session')
def db() -> Generator[DB]:
    conn = sqlite3.connect(Config.db)
    cursor = conn.cursor()

    database = DB(conn=conn, cursor=cursor)
    yield database
    
    conn.close()

@pytest.fixture(scope='function')
def delete_from_db(db):
    def _delete(table_name: Literal['user', 'employee', 'company'], obj_name):
        field_dict = {'user': 'login',
                      'employee': 'name',
                      'company': 'name'}
        if table_name not in field_dict:
            raise ValueError(f'Несуществующая таблица: {table_name}')
        field = field_dict[table_name]
        db.cursor.execute(f'SELECT * FROM {table_name} WHERE {field} = ?', (obj_name,))
        if not db.fetchone():
            raise ValueError(f'Объект {obj_name} не найден в {table_name}')
        db.cursor.execute(f'DELETE FROM {table_name} WHERE {field} = ?', (obj_name,))
        db.conn.commit()
    return _delete

@pytest.fixture(scope='function')
def db_check_obj():
    def check_name(table_name: Literal['user', 'employee', 'company'], obj_name: str):
        field_dict = {'user': 'login',
                      'employee': 'name',
                      'company': 'name'}
        conn = sqlite3.connect('course.db')
        cursor = conn.cursor()
        if table_name not in field_dict:
            raise ValueError(f'Несуществующая таблица: {table_name}')
        field = field_dict[table_name]

        cursor.execute(f'SELECT * FROM {table_name} WHERE {field} = ?', (obj_name,))
        result = cursor.fetchall()
        conn.close()
        return result
    return check_name

@pytest.fixture(scope='function')
def clean_table_db(db):
    def _clean(table_name: Literal['user', 'employee', 'company']):
        script_dict = {'user': "DELETE FROM user WHERE login != 'admin'",
                       'employee': "DELETE FROM employee",
                       'company': "DELETE FROM company"}
        if table_name not in script_dict:
            raise ValueError(f'Несуществующая таблица: {table_name}')
        script = script_dict[table_name]
        db.cursor.execute(script)
        db.conn.commit()
    return _clean
