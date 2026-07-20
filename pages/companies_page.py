from typing import Literal
from selenium.webdriver.common.by import By

from models.companies import Company
from pages.base_page import BasePage
from pages.components.header import Header


'''переписать локаторы и разделить метод на отдельные'''
class CompanyPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.header = Header(driver, self)

    PATH = '/ui/companies'
    VIEW_BUTTON = './/*[contains(@class, "eye-icon")]'
    UPDATE_INFO_BUTTON = './/*[contains(@class, "pencil-icon")]'
    DELETE_BUTTON = './/*[contains(@class, "trash-icon")]'
    MODAL_WINDOW = '//div[@class="modal-content"]'
    VIEW_MODAL = '//div[@id="viewModal"]'
    UPDATE_MODAL = '//div[@id="editModal"]'
    NAME_FIELD = './/div[@id="editCompanyName"]'
    YEAR_FIELD = './/div[@id="editYear"]'
    COUNTRY_FIELD = './/div[@id="editCountry"]'
    SUBMIT_BUTTON = '//BUTTON[@type="submit"]'
    CONTENT_WINDOW = ''

    def get_company_item(self, cmp_id: int = 2):
        return f'//div[data-company-id="{str(cmp_id)}"]'



    def open_content_window(self, cmp_id: int, button: Literal['view', 'update', 'delete']):
        options_dct = {'view': (self.VIEW_BUTTON, self.VIEW_MODAL),
                       'update': (self.UPDATE_INFO_BUTTON, self.UPDATE_MODAL),
                       'delete': (self.DELETE_BUTTON, self.DELETE_MODAL)}
        pick_button, modal = options_dct[button]
        employee = self.find_element(self.get_company_item(cmp_id))
        btn = employee.find_element(By.XPATH, pick_button)
        self.click_element(btn)
        self.wait_until_visible(modal)

    '''пересмотреть метод просмотра'''
    def view_company_data(self, cmp_id: int):
        self.open_content_window(cmp_id, 'view')
        return self.find_element('//div[@id="viewDetails"]').text


    def update_employee_data(self, cmp_id: int, company_data: Company):
        self.open_content_window(cmp_id, 'update')
        self.input_value(self.NAME_FIELD, str(company_data.name))
        self.input_value(self.YEAR_FIELD, str(company_data.year))
        self.input_value(self.COUNTRY_FIELD, str(company_data.country))
        self.click_element(self.SUBMIT_BUTTON)
        self.wait_until_invisible(self.UPDATE_MODAL)

    def delete_employee_data(self, emp_id: int):
        self.open_content_window(emp_id, 'delete')
        self.accept_alert()
        self.wait_until_visible('//body')

