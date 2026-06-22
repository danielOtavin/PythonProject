import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

@allure.feature('Домашняя страница')
class TestHome:
    @allure.story('Действия на домашней странице с данными администратора')
    @allure.title('Тестирование соответсвия данных администратора с данными на странице')
    def test_admin_info(self, admin_authorization):
        admin_data = {'ID': '1',
                      'Login': 'admin',
                      'Role': 'admin'}
        with allure.step('Получить текст информации о зарегестрированном пользователе'):
            user_info = admin_authorization.find_element(By.XPATH, '//div[@class="user-info"]').text
        with allure.step('Проверить соответсвие данных пользователя администратора с данными на странице'):
            assert admin_data['ID'] in user_info
            assert admin_data['Login'] in user_info
            assert admin_data['Role'] in user_info

    @allure.title('Тестирование выхода из домашней страницы с ролью admin')
    def test_quit(self, admin_authorization, browser):
        with allure.step('Нажать кнопку "Выйти"'):
            admin_authorization.find_element(By.XPATH, '//div[@onclick="window.logoutUser()"]').click()
            WebDriverWait(admin_authorization, 5).until(
                expected_conditions.url_contains("/ui/login")
            )
        with allure.step('Проверить наличие "login" в URL страницы'):
            assert "login" in admin_authorization.current_url