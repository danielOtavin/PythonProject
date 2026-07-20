from typing import Literal
from pages.base_page import BasePage
from pages.components.header import Header


class SQLPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.header = Header(driver, self)

    PATH = '/ui/sql'
    TEXT_AREA = '//textarea[@id="sql-input"]'
    QUERY_RADIO_BUTTON = '//input[@id="query-radio"]'
    COMMAND_RADIO_BUTTON = '//input[@id="command-radio"]'
    SEND_REQUEST_BUTTON = '//button[@id="send-request"]'

    def send_sql_query_or_command(self,  text: str, button: Literal['query', 'command']) -> None:
        selected_button = {'query': self.QUERY_RADIO_BUTTON,
                           'command': self.COMMAND_RADIO_BUTTON}
        if button not in selected_button:
            raise ValueError(f'Неизвестная кнопка: {button}')
        btn = selected_button[button]
        self.input_value(self.TEXT_AREA, text)
        self.click_element(btn)
        self.click_element(self.SEND_REQUEST_BUTTON)







