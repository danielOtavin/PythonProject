from allure import step
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
    SELECTED_ROW = './/td[text()="{emp_id}"]/..'


    @step('Отправить SQL запрос {text}')
    def send_sql_query(self, text: str) -> None:
        self.input_value((self.TEXT_AREA, text))
        self.click_element(self.QUERY_RADIO_BUTTON)
        self.click_element(self.SEND_REQUEST_BUTTON)
        self.clear_field(self.TEXT_AREA)

    @step('Отправить SQL команду {text}')
    def send_sql_command(self, text: str) -> None:
        self.input_value((self.TEXT_AREA, text))
        self.click_element(self.COMMAND_RADIO_BUTTON)
        self.click_element(self.SEND_REQUEST_BUTTON)
        self.clear_field(self.TEXT_AREA)

    @step('Проверить резульат')
    def check_result(self, emp_id: int):
        try:
            self.wait_until_visible(self.RESULT_SECTION)
            row = self.find_element(self.SELECTED_ROW.format(emp_id=emp_id))
            return row.text
        except:
            return False
