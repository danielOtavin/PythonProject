from typing import Literal
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.components.header import Header


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

    def click_button_companies(self, button: Literal['view','update','delete'], cmp_id: int = 2) -> None:
        button_name = {'view': self.VIEW_BUTTON,
                       'update': self.UPDATE_INFO_BUTTON,
                       'delete': self.DELETE_BUTTON}
        if button not in button_name:
            raise ValueError(f'Неизвестная кнопка: {button}')
        selected_button = button_name[button]
        company = self.find_element(self.get_company_item(cmp_id))
        btn = company.find_element(By.XPATH, selected_button)
        self.click_element(btn)

