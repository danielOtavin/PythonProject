from selenium.webdriver.common.by import By

from pages.components.header import Header
from allure import step


class AdminPage(Header):
    def __init__(self, driver):
        super().__init__(driver)

    PATH = '/ui/admin'
    NOTIFICATION_MESSAGE = '//div[contains(@class, "notification-message")]'
    DELETE_BUTTON = './/button[@class="delete-btn"]'
    GET_SELECT_ROLE = '//select[@id="role-select-{usr_id}"]'
    GET_ROLE_OPTION = '//select[@id="role-select-{usr_id}"]/option[@value="{role_val}"]'
    GET_ROW_PATH = '//tr[@data-user-id="{usr_id}"]'


    @step('Нажать кнопку смены роли для пользователя {user_id} на {role_value}')
    def click_role_change_button(self, user_id: int, role_value: str):
        self.click_element(self.GET_SELECT_ROLE.format(user_id = user_id))
        self.click_element(self.GET_ROLE_OPTION.format(user_id = user_id, role_value = role_value))

    @step('Нажать кнопку удаления пользователя {usr_id}')
    def click_delete_user_button(self, usr_id: int):
        row_path = self.GET_ROW_PATH.format(usr_id = usr_id)
        row = self.wait_until_visible(row_path)
        delete_button = row.find_element(By.XPATH, self.DELETE_BUTTON)
        self.click_element(delete_button)
        self.accept_alert()
        self.wait_until_invisible(row_path)