import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

@allure.feature('Страница администратора')
class TestAdmin:
    @pytest.mark.parametrize('button_xpath, expected_page',
                             [('//div[@onclick="redirectToHome()"]', '/ui/home'),
                              ('//div[@onclick="logOut()"]', '/ui/login')
                              ])
    @allure.title('Тестирование работоспособности кнопок на странице администратора')
    def test_admin_page_click_buttons(self, admin_authorization, button_xpath, expected_page):
        with allure.step('Перейти на страницу администратора'):
            admin_authorization.find_element(By.XPATH, '//a[@href="admin"]').click()
        with allure.step(f'Нажать на кнопку {button_xpath}'):
            WebDriverWait(admin_authorization, 5).until(
                expected_conditions.element_to_be_clickable((By.XPATH, button_xpath))).click()
        with allure.step(f'Проверить наличие {expected_page} в URL страницы'):
            assert expected_page in admin_authorization.current_url