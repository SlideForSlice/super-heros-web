import pytest

from app.users.dao import  UserDAO

@pytest.mark.userDAO
@pytest.mark.parametrize("user_id, user_email, is_present", [
    (1, "oleg@example.com", True),
    (2, "cringeBabai@example.com", True),
    (3,"popkinJopkin@mail.ru", False),
])
async def test_find_user_by_id(user_id, user_email, is_present):
    user = await UserDAO.find_by_id(user_id)

    if is_present:
        assert user
        assert user.id == user_id
        assert user.email == user_email
    else:
        assert not user
