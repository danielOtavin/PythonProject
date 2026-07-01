from pages.base_page import BasePage


class SQLPage(BasePage):
    text_area = '//textarea[@id="sql-input"]'
    query_radio_button = '//button[@id="query-radio"]'
    command_radio_button = '//button[@id="command-radio"]'
    send_request_button = '//button[@id="send-request"]'


    def send_sql_query(self, text: str):
        self.input_value(self.text_area, text)
        self.click_element(self.query_radio_button)
        self.click_element(self.send_request_button)


    def send_sql_command(self, text: str):
        self.input_value(self.text_area, text)
        self.click_element(self.command_radio_button)
        self.click_element(self.send_request_button)




