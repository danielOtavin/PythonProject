import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

@allure.feature('Страница администратора')
class TestAdmin:
    @allure.story('Кнопки на странице админа')
    @allure.title('Проверка работоспособности кнопок на странице админа')
    def test_admin_page_clickable_buttons(self, admin_token):
        pass



