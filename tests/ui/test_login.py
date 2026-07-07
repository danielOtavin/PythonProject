import allure
import pytest


@allure.feature("Страница авторизации")
class TestLogin:
    @allure.story('Авторизация')
    @allure.title('Тестирование авторизации пользователя на странице авторизации')
    def test_login_user_ui(self, authorization, browser):
        assert 'home' in browser.current_url

    def test_x(self, pages_admin_token):
        assert 'login' not in pages_admin_token.driver.current_url



