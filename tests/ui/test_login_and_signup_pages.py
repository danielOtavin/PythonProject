import allure
from models.users import User


@allure.feature("Страница авторизации")
class TestLoginPage:
    @allure.story('Авторизация и регистрация')
    @allure.title('Тестирование регистрации и авторизации нового пользователя')
    def test_signup_and_login_ui(self, signup_page, browser):
        user = User.random_user()
        login_page = signup_page.input_login_and_password(user.login, user.password)
        login_page.authorization(user.login, user.password)






