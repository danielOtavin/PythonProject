from enum import Enum

from allure import step
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from models.employees import Employee
from pages.components.header import Header

class OptionsButton(Enum):
    VIEW = 'view'
    UPDATE = 'update'
    DELETE = 'delete'

class EmployeePage(Header):
    def __init__(self, driver):
        super().__init__(driver)
        self.options_dct = {'view': (self.VIEW_BUTTON, self.VIEW_MODAL),
                       'update': (self.UPDATE_INFO_BUTTON, self.UPDATE_MODAL),
                       'delete': (self.DELETE_BUTTON, self.DELETE_MODAL)}

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
    EMPLOYEE_ITEM = '//div[@data-employee-id="{emp_id}"]'
    VIEW_DETAILS = '//div[@id="viewDetails"]'

    @step('Выбрать чекбокс')
    def set_checkbox(self, checkbox_locator: str, state: bool):
        checkbox = self.find_element(checkbox_locator)
        if state and not checkbox.is_selected():
            checkbox.click()
        elif not state and checkbox.is_selected():
            checkbox.click()

    @step('Открыть контентное окно')
    def open_content_window(self, emp_id: int, button: OptionsButton):
        pick_button, modal = self.options_dct[button.value]
        employee = self.find_element(self.EMPLOYEE_ITEM.format(emp_id=emp_id))
        btn = employee.find_element(By.XPATH, pick_button)
        self.click_element(btn)
        self.wait_until_visible(modal)

    @step('Закрыть модальное окно через клавишу ESC')
    def close_modal_with_esc(self):
        self.driver.find_element(By.XPATH, "//body").send_keys(Keys.ESCAPE)

    @step('Получить данные сотрудника {emp_id}')
    def view_employee_data(self, emp_id: int):
        self.open_content_window(emp_id, OptionsButton.VIEW)
        return self.find_element(self.VIEW_DETAILS).text

    @step('Обновить данные сотрудника {emp_id}')
    def update_employee_data(self, emp_id: int, employee_data: Employee) -> None:
        self.open_content_window(emp_id, OptionsButton.UPDATE)
        self.input_value((self.NAME_FIELD, str(employee_data.name)),
                         (self.SALARY_FIELD, str(employee_data.salary)))
        self.set_checkbox(self.WORK_STATUS_CHECKBOX, employee_data.work)
        self.click_element(self.SUBMIT_BUTTON)
        self.wait_until_invisible(self.CONTENT_WINDOW)

    @step('Удалить данные сотрудника {emp_id}')
    def delete_employee_data(self, emp_id: int) -> None:
        self.open_content_window(emp_id, OptionsButton.DELETE)
        self.click_element(self.CONFIRM_DELETE_BUTTON)
        self.wait_until_invisible(self.CONTENT_WINDOW)









