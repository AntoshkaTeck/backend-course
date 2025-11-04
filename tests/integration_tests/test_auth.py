from src.service.auth import AuthService


def test_decode_and_encode_access_token():
    data = {"user_id": 1}
    jwt_token = AuthService().create_access_token(data)

    assert jwt_token
    assert  isinstance(jwt_token, str)

    payload = AuthService().decode_token(jwt_token)

    assert payload
    assert payload["user_id"] == data["user_id"]

async def test_me(ac, auth_ac):
    response = await ac.get("/auth/me")
    assert response.status_code == 200
    assert response.json()["data"] == {'id': 1, 'email': 'anton.tihov.94@gmail.com'}
