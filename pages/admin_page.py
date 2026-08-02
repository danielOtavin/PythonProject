from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.components.header import Header


class AdminPage(Header):
    def __init__(self, driver):
        super().__init__(driver)

    PATH = '/ui/admin'
    NOTIFICATION_MESSAGE = '//div[contains(@class, "notification-message")]'
    DELETE_BUTTON = './/button[@class="delete-btn"]'

    def get_select_role(self, usr_id: int = 2):
        return f'//select[@id="role-select-{str(usr_id)}"]'

    def get_role_option(self, usr_id: int = 2, role_val: str = 'read'):
        return f'//select[@id="role-select-{str(usr_id)}"]/option[@value="{role_val}"]'

    def get_row_path(self, usr_id: int = 2):
        return f'//tr[@data-user-id="{str(usr_id)}"]'



    def click_role_change_button(self, user_id: int, role_value: str):
        self.click_element(self.get_select_role(user_id))
        self.click_element(self.get_role_option(user_id, role_value))


    def click_delete_user_button(self, usr_id: int):
        self.get_row_path(usr_id)
        row = self.wait_until_visible(self.get_row_path(usr_id))
        delete_button = row.find_element(By.XPATH, self.DELETE_BUTTON)
        self.click_element(delete_button)
        self.accept_alert()
        self.wait_until_invisible(self.get_row_path(usr_id))