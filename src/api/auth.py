from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Body, HTTPException, Response
from fastapi.openapi.models import Example

from pwdlib import PasswordHash
import jwt

from src.repositories.users import UsersRepository
from src.database import async_session_maker
from src.schemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix='/auth', tags=['Авторизация и Аутентификация'])

password_hash = PasswordHash.recommended()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode |= {"exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


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


@router.post('/login', summary="Аутентификация")
async def login_user(
        user_data: UserRequestAdd = Body(
            openapi_examples={
                "1": Example(
                    summary="Anton",
                    value={
                        "email": "anton.tihov.94@gmail.com",
                        "password": "qwerty12345678"
                    }
                )
            }
        ),
        response: Response = Response()
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=user_data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Неправильный логин или пароль")
        if not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Неправильный логин или пароль")
        access_token = create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)

    return {"access_token": access_token}
