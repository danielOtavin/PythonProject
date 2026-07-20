class TestHomePage:
    def test_click_buttons_home_page(self, home_page, browser):
        hp = home_page
        hp.click_button_home_page('employees')
        hp.open()
        hp.click_button_home_page('companies')
        hp.open()
        hp.click_button_home_page('sql')
        hp.open()
