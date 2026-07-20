from models.users import ADMIN, TEST


class TestHeader:
    def test_admin_token_header_pages(self, pages_admin_token):
        page = pages_admin_token
        assert ADMIN.login in page.header.get_user_info()
        page.header.click_home()
        page.wait_until_url_contains('/ui/home')
        page.header.click_quit()
        assert 'ui/login' in page.driver.current_url

    def test_user_token_header_pages(self, pages_user_token):
        page = pages_user_token
        assert TEST.login in page.header.get_user_info()
        page.header.click_home()
        page.wait_until_url_contains('/ui/home')
        page.header.click_quit()
        assert 'ui/login' in page.driver.current_url