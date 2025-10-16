from fastapi import APIRouter, Body
from fastapi.openapi.models import Example

from pwdlib import PasswordHash


from src.repositories.users import UsersRepository
from src.database import async_session_maker
from src.schemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix='/auth', tags=['Авторизация и Аутентификация'])

password_hash = PasswordHash.recommended()


@router.post('/register', summary="Добавление пользователя")
async def register_user(user_data: UserRequestAdd = Body(
    openapi_examples={
        "1": Example(
            summary="Anton",
            value={
                "email": "anton.tihov.94@gmail.com",
                "password": "qwerty12345678"
            }
        )
    }
)):
    hashed_password = password_hash.hash(user_data.password)
    new_user_data = UserAdd(email=user_data.email, hashed_password=hashed_password)

    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"satus": "OK"}
