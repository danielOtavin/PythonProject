from pages.base_page import BasePage


class HomePage(BasePage):
    employees_button = '//a[@href="/ui/employees"]'
    companies_button = '//a[@href="/ui/companies"]'
    sql_button = '//a[@href="/ui/sql"]'

    def click_employees(self):
        self.click_element(self.employees_button)
        BasePage.wait_until_url_contains(self, '/ui/employees')

    def click_companies(self):
        self.click_element(self.companies_button)
        self.wait_until_url_contains('/ui/companies')

    def click_sql(self):
        self.click_element(self.sql_button)
        self.wait_until_url_contains('/ui/sql')

