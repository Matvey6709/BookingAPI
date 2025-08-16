import pytest

from app.users.dao import UserDao


@pytest.mark.parametrize('user_id,email,is_present', [
    (1, 'fedor@moloko.ru', True),
    (2, 'sharik@moloko.ru', True),
    (7, 'asdsafdg3@sdf.com', False),
])
async def test_find_by_id(user_id, email, is_present):
    user = await UserDao.find_by_id(user_id)

    if is_present:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user
