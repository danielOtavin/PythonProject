from pages.base_page import BasePage


class SQLPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.header = Header(driver, self)

    PATH = '/ui/sql'
    TEXT_AREA = '//textarea[@id="sql-input"]'
    QUERY_RADIO_BUTTON = '//button[@id="query-radio"]'
    COMMAND_RADIO_BUTTON = '//button[@id="command-radio"]'
    SEND_REQUEST_BUTTON = '//button[@id="send-request"]'

    def send_sql_query_or_command(self,  text: str, button: Literal['query', 'command']) -> None:
        selected_button = {'query': self.QUERY_RADIO_BUTTON,
                           'command': self.COMMAND_RADIO_BUTTON}
        if button not in selected_button:
            raise ValueError(f'Неизвестная кнопка: {button}')
        btn = selected_button[button]
        self.input_value(self.TEXT_AREA, text)
        self.click_element(self.QUERY_RADIO_BUTTON)
        self.click_element(self.SEND_REQUEST_BUTTON)


    def send_sql_command(self, text: str):
        self.input_value(self.TEXT_AREA, text)
        self.click_element(self.COMMAND_RADIO_BUTTON)
        self.click_element(self.SEND_REQUEST_BUTTON)




