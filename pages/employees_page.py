from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from typing import Literal

from models.employees import Employee
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

    def get_employee_item(self, emp_id: int = 0):
        return f'//div[@data-employee-id="{str(emp_id)}"]'


    def set_checkbox(self, checkbox_locator: str, state: bool):
        checkbox = self.find_element(checkbox_locator)
        if state and not checkbox.is_selected():
            checkbox.click()
        elif not state and checkbox.is_selected():
            checkbox.click()


    def open_content_window(self, emp_id: int, button: Literal['view', 'update', 'delete']):
        options_dct = {'view': (self.VIEW_BUTTON, self.VIEW_MODAL),
                       'update': (self.UPDATE_INFO_BUTTON, self.UPDATE_MODAL),
                       'delete': (self.DELETE_BUTTON, self.DELETE_MODAL)}
        pick_button, modal = options_dct[button]
        employee = self.find_element(self.get_employee_item(emp_id))
        btn = employee.find_element(By.XPATH, pick_button)
        self.click_element(btn)
        self.wait_until_visible(modal)


    def close_modal_with_esc(self):
        self.driver.find_element(By.XPATH, "//body").send_keys(Keys.ESCAPE)


    def view_employee_data(self, emp_id: int):
        self.open_content_window(emp_id, 'view')
        return self.find_element('//div[@id="viewDetails"]').text


    def update_employee_data(self, emp_id: int, employee_data: Employee) -> None:
        self.open_content_window(emp_id, 'update')
        self.input_value(self.NAME_FIELD, str(employee_data.name))
        self.input_value(self.SALARY_FIELD, str(employee_data.salary))
        self.set_checkbox(self.WORK_STATUS_CHECKBOX, employee_data.work)
        self.click_element(self.SUBMIT_BUTTON)
        self.wait_until_invisible(self.CONTENT_WINDOW)

    def delete_employee_data(self, emp_id: int) -> None:
        self.open_content_window(emp_id, 'delete')
        self.click_element(self.CONFIRM_DELETE_BUTTON)
        self.wait_until_invisible(self.CONTENT_WINDOW)









