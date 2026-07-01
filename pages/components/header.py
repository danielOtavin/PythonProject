from pages.base_page import BasePage


class Header(BasePage):
    home_button = '//div[@onclick="redirectToHome()"]'
    quit_button = '//div[@onclick="windowLogoutUser()"]'
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
