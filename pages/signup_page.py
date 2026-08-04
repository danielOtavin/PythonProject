from allure import step
from pages.base_page import BasePage
from pages.login_page_ import LoginPage


class SignupPage(BasePage):
    PATH = '/ui/user/signup'
    EMAIL_FIELD = '//input[@id="email"]'
    EMAIL_ERROR = '//.class[id="email-error"]'
    PASSWORD_FIELD = '//input[@id="password"]'
    PASSWORD_ERROR = '//.class[id="password-error"]'
    SUBMIT_BUTTON = '//input[@type="submit"]'

    @step('Зарегистрироваться с логином {login} и паролем {password}')
    def registration(self, email: str, password: str):
        self.input_value([(self.EMAIL_FIELD, email),
                        (self.PASSWORD_FIELD, password)])
        self.click_element(self.SUBMIT_BUTTON)
        self.accept_alert()
        return LoginPage(self.driver)



