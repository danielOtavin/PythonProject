from typing import Literal

from pages.components.header import Header
from allure import step

class HomePage(Header):
    def __init__(self, driver):
        super().__init__(driver)
        self.selected_button = {'employees': (self.EMPLOYEES_BUTTON, '/ui/employees'),
                                'companies': (self.COMPANIES_BUTTON, '/ui/companies'),
                                'sql': (self.SQL_BUTTON, '/ui/sql')
                                }

    PATH = '/ui/home'
    EMPLOYEES_BUTTON = '//a[@href="/ui/employees"]'
    COMPANIES_BUTTON = '//a[@href="/ui/companies"]'
    SQL_BUTTON = '//a[@href="/ui/sql"]'

    @step('Нажать кнопку {button} на Домашней странице')
    def click_button_home_page(self, button: Literal['employees', 'companies', 'sql']) -> None:
        locator, url = self.selected_button[button]
        self.click_element(locator)
        self.wait_until_url_contains(url)

