from selenium.webdriver.common.by import By
from typing import Literal

from pages.base_page import BasePage
from pages.components.header import Header


class EmployeePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.header = Header(driver, self)

    PATH = '/ui/employees'
    VIEW_BUTTON = './/*[contains(@class, "eye-icon")]'
    UPDATE_INFO_BUTTON = './/*[contains(@class, "pencil-icon")]'
    DELETE_BUTTON = './/*[contains(@class, "trash-icon")]'
    CONTENT_WINDOW = '//div[@class="modal-content"]'
    NAME_FIELD = '//input[@id="editName"]'
    SALARY_FIELD = '//input[@id="editSalary"]'
    WORK_STATUS_CHECKBOX = '//input[@id="editWorkStatus"]'
    SUBMIT_BUTTON = '//button[@type="submit"]'
    CONFIRM_DELETE_BUTTON = '//button[@id="confirmDeleteBtn"]'
    CANCEL_DELETE_BUTTON = '//button[@id="cancelDeleteBtn"]'
    VIEW_MODAL = '//div[@id="viewModal"]'
    UPDATE_MODAL = '//div[@id="editModal"]'
    DELETE_MODAL = '//div[@id="deleteModal"]'

    def get_employee_item(self, emp_id: int = 2) -> str:
        return f'//div[@data-employee-id="{str(emp_id)}"]'

    def click_button_employees(self, button: Literal['view','update','delete'], emp_id: int = 2) -> None:
        button_name = {'view': self.VIEW_BUTTON,
                       'update': self.UPDATE_INFO_BUTTON,
                       'delete': self.DELETE_BUTTON}
        if button not in button_name:
            raise ValueError(f'Неизвестная кнопка: {button}')
        selected_button = button_name[button]
        employee = self.find_element(self.get_employee_item(emp_id))
        btn = employee.find_element(By.XPATH, selected_button)
        self.click_element(btn)



