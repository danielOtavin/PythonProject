from pages.base_page import BasePage
from pages.home_page import HomePage


class LoginPage(BasePage):
    username = '//input[@name="username"]'
    password = '//input[@name="password"]'
    login_button = '//button[@onclick="handleLogin()"]'
    new_user_registration_button = '//a[@href="user/signup"]'

    def authorization(self, login: str, password: str):
        self.input_value(self.username, login)
        self.input_value(self.password, password)
        self.click_element(self.login_button)
        self.accept_alert()
        self.wait_until_url_contains('/ui/home')
        return HomePage(self.driver)
