import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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
                EC.element_to_be_clickable((By.XPATH, button_xpath))).click()
        with allure.step(f'Проверить наличие {expected_page} в URL страницы'):
            assert expected_page in admin_authorization.current_url

    @pytest.mark.skip
    @allure.title('')
    def test_user_update_role_and_delete(self, admin_authorization, random_user):
        with allure.step('Получить ID пользователя'):
            user_id = random_user.id
        with allure.step('Перейти на страницу администратора'):
            admin_authorization.find_element(By.XPATH, '//a[@href="admin"]').click()
        with allure.step(f'Найти строку пользователя с ID {user_id}'):
            row = WebDriverWait(admin_authorization, 5).until(
                EC.presence_of_element_located((By.XPATH, f'//tr[@data-user-id="{user_id}"]'))
            )
        with allure.step(f'Сменить роль пользователя'):
            select_element = row.find_element(By.XPATH, f'//select[@id="role-select-{user_id}"]')
            WebDriverWait(row, 5).until(
                EC.element_to_be_clickable((By.XPATH, f'//select[@id="role-select-{user_id}"]/option[@value="write"]'))).click()
            assert select_element.get_attribute('value') == 'write'
        with allure.step('Проверить наличие уведомления об изменении роли пользователя'):
            notification = WebDriverWait(admin_authorization, 5).until(
                EC.visibility_of_element_located((By.XPATH, '//div[@class="notification-message"]'))
            )
            assert notification.is_displayed() is True
        with allure.step('Дождаться закрытия уведомления'):
            WebDriverWait(admin_authorization, 10).until(
                EC.invisibility_of_element_located((By.XPATH, '//div[@class="notification hidden"'))
            )
        with allure.step('Нажать кнопку удаления пользователя'):
            WebDriverWait(row, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@class="delete-btn"]'))).click()


