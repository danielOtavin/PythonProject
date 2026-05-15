from main import Token


class TestTokenPositive:
    def test_admin_token_positive(self, admin_auth):
        result = admin_auth
        assert result.get('Authorization') is not None

    def test_user_token_positive(self, user_token):
        result = user_token
        assert result.get('Authorization') is not None

class TestTokenNegative:
    def test_admin_token_negative(self):
        unknown_user_token = Token()
        result = unknown_user_token.get_token('notadmin', 'notadmin')
        assert result is None

    def test_user_token_negative(self):
        unknown_user = Token()
        result = unknown_user.get_token('a@mail.ru', 'aaaaa')
        assert result is None

    def test_incorrect_len_password(self):
        token = Token()
        result = token.get_token('a@mail.ru', '')
        assert result is None

