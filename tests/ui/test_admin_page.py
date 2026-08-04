import allure
import pytest

from models.users import ADMIN, User
from pages.admin_page import AdminPage


@allure.feature('Страница администратора')
class TestAdminPage:
    @allure.title('')
    def test_admin_page_user_role_change(self, admin_token, pages_admin_token,
                                                         user_api, db_check_obj):
        user_data = User.random_user()
        user = user_api.create(user_data, admin_token)
        assert len(db_check_obj('user', user.login)) > 0
        admin_page = pages_admin_token(AdminPage)
        admin_page.click_role_change_button(user.id, 'write')
        user_role = admin_page.find_element(admin_page.get_select_role(user.id))
        res = user_role.get_attribute('value')
        assert res == 'write'


    @pytest.mark.parametrize('open_page', [(AdminPage, ADMIN)], indirect=True)
    def test_admin_page_delete_user(self, admin_token, open_page, user_api, db_check_obj):
        user_data = User.random_user()
        user = user_api.create(user_data, admin_token)
        assert len(db_check_obj('user', user.login)) > 0

        open_page.driver.refresh()
        open_page.click_delete_user_button(user.id)
        assert len(db_check_obj('user', user.login)) == 0
