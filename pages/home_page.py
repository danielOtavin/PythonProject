from pages.base_page import BasePage


class HomePage(BasePage):
    PATH = '/ui/home'
    EMPLOYEES_BUTTON = '//a[@href="/ui/employees"]'
    COMPANIES_BUTTON = '//a[@href="/ui/companies"]'
    SQL_BUTTON = '//a[@href="/ui/sql"]'

    def click_employees(self):
        self.click_element(self.EMPLOYEES_BUTTON)
        BasePage.wait_until_url_contains(self, '/ui/employees')

    def click_button_home_page(self, button: Literal['employees', 'companies', 'sql']) -> None:
        selected_button = {'employees': (self.EMPLOYEES_BUTTON, '/ui/employees'),
                           'companies': (self.COMPANIES_BUTTON, '/ui/companies'),
                           'sql': (self.SQL_BUTTON, '/ui/sql')}
        if button not in selected_button:
            raise ValueError(f'Неизвестная кнопка: {button}')
        locator, url = selected_button[button]
        self.click_element(locator)
        self.wait_until_url_contains(url)

