from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class EmployeePage(BasePage):
    PATH = '/ui/employees'
    VIEW_BUTTON = './/svg[@class="icon eye-icon"]'
    UPDATE_INFO_BUTTON = './/svg[@class="icon pencil-icon  "]'
    DELETE_BUTTON = './/svg[@class="icon trash-icon  "]'

    def get_employee_item(self, emp_id: int = 2) -> str:
        return f'//div[@data-employee-id="{str(emp_id)}"]'

    def click_view_button(self, emp_id: int) -> None:
        employee = self.find_element(self.get_employee_item(emp_id))
        button = employee.find_element(By.XPATH, self.VIEW_BUTTON)
        self.click_element(button)

    def click_update_info_button(self, emp_id: int) -> None:
        employee = self.find_element(self.get_employee_item(emp_id))
        button = employee.find_element(By.XPATH, self.UPDATE_INFO_BUTTON)
        self.click_element(button)

    def click_delete_button(self, emp_id: int) -> None:
        employee = self.find_element(self.get_employee_item(emp_id))
        button = employee.find_element(By.XPATH, self.DELETE_BUTTON)
        self.click_element(button)



