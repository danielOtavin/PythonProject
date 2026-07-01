from pages.base_page import BasePage


class SignupPage(BasePage):
    email_field = '//input[@id="email"]'
    password_field = '//input[@id="password"]'
    submit_button = '//input[@type="submit"]'

    def input_login_and_password(self, email: str, password: str):
        self.input_value(self.email_field, email)
        self.input_value(self.password_field, password)
        self.click_element(self.submit_button)


