import allure


@allure.feature("Страница авторизации")
class TestLogin:
    @allure.story('Авторизация')
    @allure.title('Тестирование регистрации и авторизации нового пользователя на странице авторизации')
    def test_registration_new_user_and_authorization(self, browser, registration_user_with_role_read,
                                                     basic_authorization):
        with allure.step('Зарегестировать пользователя с ролью read'):
            browser, login, password = registration_user_with_role_read
        with allure.step('Проверить переход на страницу авторизации'):
            assert "login" in browser.current_url
        with allure.step('Авторизоваться с данными зарегестированного пользователя'):
            basic_authorization(login, password)
        with allure.step('Проверить переход на домашнюю страницу'):
            assert "home" in browser.current_url




