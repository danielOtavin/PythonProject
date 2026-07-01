from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class AdminPage(BasePage):
    def get_select_role(self, usr_id: int = 2):
        return f'//select[@id="role-select-{str(usr_id)}"]'

    def get_role_option(self, usr_id: int = 2, role_val: str = 'read'):
        return f'//select[@id="role-select-{str(usr_id)}"]/option[@value={role_val}]'


    def click_role_change_button(self, usr_id: int, role_val: str):
        self.click_element(self.get_role_option(usr_id=usr_id, role_val=role_val))
        self.wait_until_visible('//div[@class="notification-message"]')
        self.wait_until_invisible('//div[@class="notification hidden"]')

    def click_delete_user_button(self, usr_id: int):
        row_path = f'//tr[@data-user-id="{str(usr_id)}"]'
        row = self.wait_until_visible(row_path)
        delete_button = row.find_element(By.XPATH, f'.//button[@class="delete-btn"]')
        self.click_element(delete_button)
        self.accept_alert()
        self.wait_until_invisible(row_path)