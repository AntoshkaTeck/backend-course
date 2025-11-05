import pytest


@pytest.mark.parametrize("user_data, status_code", [
    ({"email": "", "password": ""}, 422),
    ({"email": "test@test", "password": "1234"}, 422),
    ({"email": "test@test.ru", "password": "1234"}, 200),
    ({"email": "test@test.ru", "password": "1234"}, 403),
])
async def test_register(user_data, status_code, ac):
    response = await ac.post("/auth/register", json=user_data)
    assert response.status_code == status_code
    if response.status_code == 200:
        res = response.json()
        assert res["status"] == "OK"


@pytest.mark.parametrize("user_data, status_code", [
    ({"email": "", "password": ""}, 422),
    ({"email": "test@test.ru", "password": "1234"}, 200),
    ({"email": "test@test.ru", "password": "1111"}, 401),
])
async def test_login_user(user_data, status_code, ac):
    response = await ac.post("/auth/login", json=user_data)
    assert response.status_code == status_code
    if response.status_code == 200:
        assert "access_token" in ac.cookies


@pytest.mark.parametrize("user_data", [
    ({"email": "test@test.ru"}),
])
async def test_logged_me(user_data, ac):
    response = await ac.get("/auth/me")
    res = response.json()
    assert "data" in res
    assert res["data"]["email"] == user_data["email"]


async def test_logout(ac):
    response = await ac.post("/auth/logout")
    res = response.json()
    assert res["status"] == "OK"


async def test_logout_me(ac):
    response = await ac.get("/auth/me")
    assert response.status_code == 401
