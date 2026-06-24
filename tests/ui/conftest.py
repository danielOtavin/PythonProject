import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from users import User


@pytest.fixture(scope='function')
def browser():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture(scope='function')
def registration_user_with_role_read(browser):
    user = User.random_user()
    login = user.login
    password = user.password
    browser.get('http://127.0.0.1:8010/ui/login')
    browser.find_element(By.XPATH, "//a[@href='user/signup']").click()
    WebDriverWait(browser, 10).until(
        expected_conditions.url_contains('/ui/user/signup')
    )
    browser.find_element(By.XPATH, "//input[@id='email']").send_keys(login)
    browser.find_element(By.XPATH, "//input[@id='password']").send_keys(password)
    browser.find_element(By.XPATH, "//input[@value='Зарегистрироваться']").click()
    WebDriverWait(browser, 10).until(
        expected_conditions.alert_is_present()
    )
    browser.switch_to.alert.accept()
    WebDriverWait(browser, 10).until(
        expected_conditions.url_contains("/ui/login")
    )
    yield browser, login, password

@pytest.fixture(scope='function')
def basic_authorization(browser):
    def _login(login: str, password: str):
        browser.find_element(By.NAME, 'username').send_keys(login)
        browser.find_element(By.NAME, 'password').send_keys(password)
        browser.find_element(By.XPATH, "//button[@onclick='handleLogin()']").click()
        WebDriverWait(browser, 3).until(expected_conditions.alert_is_present())
        browser.switch_to.alert.accept()
        WebDriverWait(browser, 5).until(
            expected_conditions.url_contains("/ui/home")
        )
        return browser
    yield _login


@pytest.fixture(scope='function')
def admin_authorization(browser):
    browser.get('http://127.0.0.1:8010/ui/login')
    browser.find_element(By.NAME, 'username').send_keys('admin')
    browser.find_element(By.NAME, 'password').send_keys('admin')
    browser.find_element(By.XPATH, "//button[@onclick='handleLogin()']").click()
    WebDriverWait(browser, 3).until(expected_conditions.alert_is_present())
    browser.switch_to.alert.accept()
    WebDriverWait(browser, 5).until(
        expected_conditions.url_contains("/ui/home")
    )

    yield browser