import allure

from models.users import User, ADMIN, TEST


@allure.feature("Страница авторизации")
class TestLogin:
    @allure.story('Авторизация и регистрация')
    @allure.title('Тестирование регистрации и авторизации нового пользователя')
    def test_signup_ui(self, signup_page, browser, clean_db):
        user = User.random_user()
        login_page = signup_page.input_login_and_password(user.login, user.password)
        login_page.authorization(user.login, user.password)

    # def test_login_ui(self, login_page, browser):
    #     home_page_admin = login_page.authorization(ADMIN.login, ADMIN.password)
    #     assert ADMIN.login in home_page_admin.header.get_user_info()
    #     home_page_admin.header.click_quit()
    #     home_page_user = login_page.authorization(TEST.login, TEST.password)
    #     assert TEST.login in home_page_user.header.get_user_info()







