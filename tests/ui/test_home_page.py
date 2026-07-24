import pytest


class TestHomePage:
    @pytest.mark.parametrize('button, url', [('employees', '/ui/employees'),
                                        ('companies', '/ui/companies'),
                                        ('sql', '/ui/sql')]
                             )
    def test_click_buttons_home_page(self, home_page, browser, button, url):
        hp = home_page
        hp.click_button_home_page(button)
        assert url in browser.current_url
