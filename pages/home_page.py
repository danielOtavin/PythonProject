from pages.base_page import BasePage


class HomePage(BasePage):
    PATH = '/ui/home'
    EMPLOYEES_BUTTON = '//a[@href="/ui/employees"]'
    COMPANIES_BUTTON = '//a[@href="/ui/companies"]'
    SQL_BUTTON = '//a[@href="/ui/sql"]'

    def click_employees(self):
        self.click_element(self.EMPLOYEES_BUTTON)
        BasePage.wait_until_url_contains(self, '/ui/employees')

    def click_companies(self):
        self.click_element(self.COMPANIES_BUTTON)
        self.wait_until_url_contains('/ui/companies')

    def click_sql(self):
        self.click_element(self.SQL_BUTTON)
        self.wait_until_url_contains('/ui/sql')

