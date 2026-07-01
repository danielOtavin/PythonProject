from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class EmployeePage(BasePage):
    view_button = './/svg[@class="icon eye-icon"]'
    update_info_button = './/svg[@class="icon pencil-icon  "]'
    delete_button = './/svg[@class="icon trash-icon  "]'

    def get_employee_item(self, emp_id: int = 2) -> str:
        return f'//div[@data-employee-id="{str(emp_id)}"]'

    def click_view_button(self, emp_id: int) -> None:
        employee = self.find_element(self.get_employee_item(emp_id))
        button = employee.find_element(By.XPATH, self.view_button)
        self.click_element(button)

    def click_update_info_button(self, emp_id: int) -> None:
        employee = self.find_element(self.get_employee_item(emp_id))
        button = employee.find_element(By.XPATH, self.update_info_button)
        self.click_element(button)

    def click_delete_button(self, emp_id: int) -> None:
        employee = self.find_element(self.get_employee_item(emp_id))
        button = employee.find_element(By.XPATH, self.delete_button)
        self.click_element(button)



