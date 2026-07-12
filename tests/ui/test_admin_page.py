import allure

from models.users import ADMIN, User


@allure.feature('Страница администратора')
class TestAdminPage:
    @allure.title('')
    def test_admin_page_user_role_change_and_delete_user(self, admin_token, page_specific_admin_token, user_api, db_check_obj):
        user_data = User.random_user()
        user = user_api.create(user_data, admin_token)
        assert len(db_check_obj('user', user.login)) > 0
        admin_page = page_specific_admin_token('AdminPage')
        admin_page.click_role_change_button(user.id, 'read')
        admin_page.click_delete_user_button(user.id)
        assert len(db_check_obj('user', user.login)) == 0
