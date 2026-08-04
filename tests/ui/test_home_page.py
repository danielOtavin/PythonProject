import allure
import pytest
from pytest import mark


@mark.home_page
class TestHomePage:
    @pytest.mark.parametrize('button, url', [('employees', '/ui/employees'),
                                        ('companies', '/ui/companies'),
                                        ('sql', '/ui/sql')])
    def test_click_buttons_home_page(self, home_page, browser, button, url):
        with allure.step('Открыть домашнюю страницу'):
            hp = home_page
        with allure.step(f'Нажать кнопку {button} на странице'):
            hp.click_button_home_page(button)
        with allure.step(f'Текущий URL страницы соответствует URL страницы {url}'):
            assert url in browser.current_url
