from pages.base_page import BasePage
from pages.home_page import HomePage


class LoginPage(BasePage):
    PATH = '/ui/login'
    USERNAME = '//input[@name="username"]'
    PASSWORD = '//input[@name="password"]'
    LOGIN_BUTTON = '//button[@onclick="handleLogin()"]'
    NEW_USER_REGISTRATION_BUTTON = '//a[@href="user/signup"]'

    def authorization(self, login: str, password: str):
        self.input_value(self.USERNAME, login)
        self.input_value(self.PASSWORD, password)
        self.click_element(self.LOGIN_BUTTON)
        self.accept_alert()
        self.wait_until_url_contains('/ui/home')
        return HomePage(self.driver)
