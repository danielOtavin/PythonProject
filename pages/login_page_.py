from allure import step
from pages.components.header import Header
from pages.home_page import HomePage


class LoginPage(Header):
    def __init__(self, driver):
        super().__init__(driver)

    PATH = '/ui/login'
    USERNAME = '//input[@name="username"]'
    PASSWORD = '//input[@name="password"]'
    LOGIN_BUTTON = '//button[@onclick="handleLogin()"]'
    NEW_USER_REGISTRATION_BUTTON = '//a[@href="user/signup"]'

    @step('Авторизоваться с логином {login} и паролем {password}')
    def authorization(self, login: str, password: str) -> HomePage:
        self.input_value([(self.USERNAME, login),
                          (self.PASSWORD, password)])
        self.click_element(self.LOGIN_BUTTON)
        self.accept_alert()
        self.wait_until_url_contains(HomePage.PATH)
        return HomePage(self.driver)
