import pytest
from httpx import AsyncClient
from app.tests.conftest import get_current_user


@pytest.mark.parametrize('email,password,status_code', [
    ('kot@pes.com', 'kotopes', 200),
    ('kot@pes.com', 'kot0pes', 409),
    ('pes@pes.com', 'kot0pes', 200),
    ('abc', 'kot0pes', 422),
])
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post('/auth/register', json={
        'email': email,
        'password': password,
    })

    assert response.status_code == status_code


@pytest.mark.parametrize('email,password,status_code', [
    ('test@test.com', 'test', 200),
    ('test2@test.com', 'test', 200),
    ('wrong@wrong.com', 'test', 401),
])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post('/auth/login', json={
        'email': email,
        'password': password,
    })
    res = await get_current_user()
    print(res)
    assert response.status_code == status_code
