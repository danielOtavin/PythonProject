from pages.base_page import BasePage


class SignupPage(BasePage):
    PATH = '/ui/user/signup'
    EMAIL_FIELD = '//input[@id="email"]'
    PASSWORD_FIELD = '//input[@id="password"]'
    SUBMIT_BUTTON = '//input[@type="submit"]'

    def input_login_and_password(self, email: str, password: str):
        self.input_value(self.EMAIL_FIELD, email)
        self.input_value(self.PASSWORD_FIELD, password)
        self.click_element(self.SUBMIT_BUTTON)


