import allure
from models.users import User


@allure.feature("Страница авторизации")
class TestLoginPage:
    @allure.story('Авторизация и регистрация')
    @allure.title('Тестирование регистрации и авторизации нового пользователя')
    def test_signup_and_login_ui(self, signup_page, browser):
        with allure.step('Создать данные пользователя'):
            user = User.random_user()
        with allure.step('Ввести данные пользователя на странице создания пользователя'):
            login_page = signup_page.registration(user.login, user.password)
        with allure.step('Авторизоваться с данными пользователя'):
            login_page.authorization(user.login, user.password)






