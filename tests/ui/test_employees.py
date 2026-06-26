import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class TestEmployees:
    def test_page_employees_click_buttons(self, admin_authorization):
        with allure.step('Проверить работоспособность кнопки перехода на страницу работы с сотрудниками'):
            admin_authorization.find_element(By.XPATH, '//a[@href="/ui/employees"]').click()
            assert '/ui/employees' in admin_authorization.current_url
        with allure.step('Проверить работоспособность кнопки домой'):
            admin_authorization.find_element(By.XPATH, '//div[@class="home-button"]').click()
            assert '/ui/home' in admin_authorization.current_url
        with allure.step('Вернуться на страницу работы с сотрудниками'):
            admin_authorization.find_element(By.XPATH, '//a[@href="/ui/employees"]').click()
            assert '/ui/employees' in admin_authorization.current_url
        with allure.step('Проверить работоспособность кнопки выхода'):
            admin_authorization.find_element(By.XPATH, '//div[@class="logout-button"]').click()
            assert '/ui/login' in admin_authorization.current_url
