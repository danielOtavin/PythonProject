from typing import Literal

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.components.header import Header


class SQLPage(Header):
    def __init__(self, driver):
        super().__init__(driver)

    PATH = '/ui/sql'
    TEXT_AREA = '//textarea[@id="sql-input"]'
    QUERY_RADIO_BUTTON = '//input[@id="query-radio"]'
    COMMAND_RADIO_BUTTON = '//input[@id="command-radio"]'
    SEND_REQUEST_BUTTON = '//button[@id="send-request"]'
    RESULT_SECTION = '//DIV[@id="result-section"]'



    def send_sql_query(self, text: str) -> None:
        self.input_value(self.TEXT_AREA, text)
        self.click_element(self.QUERY_RADIO_BUTTON)
        self.click_element(self.SEND_REQUEST_BUTTON)
        self.clear_field(self.TEXT_AREA)

    def send_sql_command(self, text: str) -> None:
        self.input_value(self.TEXT_AREA, text)
        self.click_element(self.COMMAND_RADIO_BUTTON)
        self.click_element(self.SEND_REQUEST_BUTTON)
        self.clear_field(self.TEXT_AREA)


    def check_result(self, emp_id: int):
        try:
            self.wait_until_visible(self.RESULT_SECTION)
            row = self.find_element(f'.//td[text()="{emp_id}"]/..')
            return row.text
        except:
            return False
