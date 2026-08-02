from typing import Literal
from enum import Enum
from selenium.webdriver.common.by import By
from webdriver_manager.core import driver

from models.companies import Company
from pages.base_page import BasePage
from pages.components.header import Header


class ContentButton(Enum):
    UPDATE = "update"
    VIEW = "view"
    DELETE = "DELETE"
    

'''переписать локаторы и разделить метод на отдельные'''
class CompanyPage(Header):
    def __init__(self, driver):
        super().__init__(driver)
        self.options =  {
                            'view': (self.VIEW_BUTTON, self.VIEW_MODAL),
                            'update': (self.UPDATE_INFO_BUTTON, self.UPDATE_MODAL)
                        }

    PATH = '/ui/companies'
    VIEW_BUTTON = './/*[contains(@class, "eye-icon")]'
    UPDATE_INFO_BUTTON = './/*[contains(@class, "pencil-icon")]'
    DELETE_BUTTON = './/*[contains(@class, "trash-icon")]'
    MODAL_WINDOW = '//div[@class="modal-content"]'
    VIEW_MODAL = '//div[@id="viewModal"]'
    UPDATE_MODAL = '//div[@id="editModal"]'
    NAME_FIELD = '//input[@id="editCompanyName"]'
    YEAR_FIELD = '//input[@id="editYear"]'
    COUNTRY_FIELD = '//input[@id="editCountry"]'
    SUBMIT_BUTTON = '//BUTTON[@type="submit"]'
    DELETE_EMPLOYEE_VIEW = './/*[contains(@class, "icon remove-icon")]'
    COMPANY_ITEM_BY_ID = '//div[@data-company-id="{cmp_id}"]'

    def get_company_item(self, cmp_id: int):
        return self.COMPANY_ITEM_BY_ID.format(cmp_id=cmp_id)
    
    def open_content_window(self, cmp_id: int, button: ContentButton):
        company_card = self.find_element(self.get_company_item(cmp_id))

        if button == 'delete':
            btn = company_card.find_element(By.XPATH, self.DELETE_BUTTON)
            self.click_element(btn)
            self.accept_alert()
        else:
           
            pick_button, modal = self.options[button]
            btn = company_card.find_element(By.XPATH, pick_button)
            self.click_element(btn)
            self.wait_until_visible(modal)

    def view_company_data(self, cmp_id: int):
        self.open_content_window(cmp_id, 'view')
        return self.find_element(self.VIEW_MODAL).text

    def delete_employee_from_company_via_view_window(self, cmp_id: int, emp_id: int):
        self.view_company_data(cmp_id)
        row = self.driver.find_element(By.XPATH, f'//tr[@data-id="{emp_id}"]')
        remove_icon = row.find_element(By.XPATH, self.DELETE_EMPLOYEE_VIEW)
        self.click_element(remove_icon)
        self.accept_alert()
        self.wait_until_invisible(f'//tr[@data-id="{emp_id}"]')

    def update_company_data(self, cmp_id: int, company_data: Company):
        self.open_content_window(cmp_id, 'update')
        self.clear_field(self.NAME_FIELD)
        self.input_value(self.NAME_FIELD, str(company_data.name))
        self.clear_field(self.YEAR_FIELD)
        self.input_value(self.YEAR_FIELD, str(company_data.year))
        self.clear_field(self.COUNTRY_FIELD)
        self.input_value(self.COUNTRY_FIELD, str(company_data.country))
        self.click_element(self.SUBMIT_BUTTON)
        self.wait_until_invisible(self.UPDATE_MODAL)

    def delete_company_data(self, cmp_id: int):
        self.open_content_window(cmp_id, 'delete')
        self.accept_alert()
        self.wait_until_invisible(f'//tr[@data-id="{cmp_id}"]')




