from pages.base_page import BasePage


class Header(BasePage):
    def __init__(self, driver):
        super().__init__(driver=driver)

    home_button = '//div[@class="home-button"]'
    quit_button = '//div[@class="logout-button"]'
    user_info = '//div[@class="user-info"]'
    admin_button = '//a[@href="admin"]'

    def click_quit(self):
        self.click_element(self.quit_button)
        self.wait_until_url_contains('/ui/login')

    def get_user_info(self):
        return self.get_text(self.user_info)

    def click_admin(self):
        self.click_element(self.admin_button)
        self.wait_until_url_contains('/ui/admin')

    def click_home(self):
        self.click_element(self.home_button)
        self.wait_until_url_contains('/ui/home')
