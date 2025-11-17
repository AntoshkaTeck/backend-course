from fastapi import APIRouter, Body, Response
from fastapi.openapi.models import Example

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import (
    UserAlreadyExistsException,
    UserAlreadyExistsHTTPException,
    UserNotFoundException,
    IncorrectPasswordException,
    IncorrectPasswordHTTPException,
)
from src.schemas.users import UserRequestAdd
from src.service.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и Аутентификация"])


@router.post("/register", summary="👥 Добавление пользователя")
async def register_user(
    db: DBDep,
    user_data: UserRequestAdd = Body(
        openapi_examples={
            "1": Example(
                summary="Anton",
                value={"email": "anton.tihov.94@gmail.com", "password": "qwerty12345678"},
            )
        }
    ),
):
    try:
        await AuthService(db).register_user(user_data)
    except UserAlreadyExistsException:
        raise UserAlreadyExistsHTTPException
    return {"status": "OK"}


@router.post("/login", summary="✅ Аутентификация")
async def login_user(
    db: DBDep,
    response: Response,
    user_data: UserRequestAdd = Body(
        openapi_examples={
            "1": Example(
                summary="Anton",
                value={"email": "anton.tihov.94@gmail.com", "password": "qwerty12345678"},
            )
        }
    ),
):
    try:
        access_token = await AuthService(db).login_user(user_data)
    except (IncorrectPasswordException, UserNotFoundException):
        raise IncorrectPasswordHTTPException

    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.post("/logout", summary="🚪 Выход из системы")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}


@router.get("/me", summary="👤 Текущий авторизованный пользователь")
async def get_me(db: DBDep, user_id: UserIdDep):
    user = await AuthService(db).get_me(user_id=user_id)
    return {"data": user}
