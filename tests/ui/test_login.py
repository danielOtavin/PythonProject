import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from users import User


@allure.feature("Страница авторизации")
class TestLogin:
    @allure.story('Авторизация')
    @allure.title('Тестирование регистрации и авторизации нового пользователя на странице авторизации')
    def test_registration_new_user_and_authorization(self, browser, registration_user_with_role_read,
                                                     basic_authorization):
        browser, login, password = registration_user_with_role_read
        assert "login" in browser.current_url
        basic_authorization(login, password)
        assert "home" in browser.current_url




