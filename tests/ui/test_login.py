import allure
import pytest


@allure.feature("Страница авторизации")
class TestLogin:
    @allure.story('Авторизация')
    @allure.title('Тестирование авторизации пользователя на странице авторизации')
    @pytest.mark.parametrize('authorization_fixture', [
        'authorization_admin',
        'authorization_user',
    ])
    def test_login_user_ui(self, authorization_fixture, browser, request):
        authorized_page = request.getfixturevalue(authorization_fixture)
        assert 'home' in authorized_page.driver.current_url




