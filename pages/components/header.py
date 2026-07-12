class Header:
    def __init__(self, driver, page):
        self.driver = driver
        self.page = page

    home_button = '//div[@class="home-button"]'
    quit_button = '//div[@class="logout-button"]'
    user_info = '//div[@class="user-info"]'
    admin_button = '//a[@href="admin"]'

    def click_quit(self):
        self.page.click_element(self.quit_button)
        self.page.wait_until_url_contains('/ui/login')

    def get_user_info(self):
        return self.page.get_text(self.user_info)

    def click_admin(self):
        self.page.click_element(self.admin_button)
        self.page.wait_until_url_contains('/ui/admin')

    def click_home(self):
        self.page.click_element(self.home_button)
        self.page.wait_until_url_contains('/ui/home')
