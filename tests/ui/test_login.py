import allure
import pytest


@allure.feature("Страница авторизации")
class TestLogin:
    @allure.story('Авторизация')
    @allure.title('Тестирование авторизации пользователя на странице авторизации')
    # @pytest.mark.parametrize('authorization_fixture', [
    #     'authorization_admin',
    #     'authorization_user',
    # ])
    def test_login_user_ui(self, authorization, browser):
        assert 'home' in browser.current_url



