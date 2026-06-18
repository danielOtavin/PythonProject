

import pytest
from users import User

def test_simple_way(user_with_role: User):
    print("test_simple_way")
    print(user_with_role)

@pytest.mark.parametrize("user_with_role", ["WRITE", "ADMIN", "READ", "WRITE", "ADMIN"], indirect=True)
def test_parametrize_fixture(user_with_role: User):
    print("test_parametrize_fixture")
    print(user_with_role)