from fastapi import APIRouter, Body, HTTPException, Response
from fastapi.openapi.models import Example

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import UserAlreadyExistException
from src.schemas.users import UserRequestAdd, UserAdd
from src.service.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и Аутентификация"])


@router.post("/register", summary="Добавление пользователя")
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
    hashed_password = AuthService().hash_password(user_data.password)
    new_user_data = UserAdd(email=user_data.email, hashed_password=hashed_password)

    try:
        await db.users.add(new_user_data)
        await db.commit()
        return {"status": "OK"}
    except UserAlreadyExistException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)


@router.post("/login", summary="Аутентификация")
async def login_user(
    db: DBDep,
    user_data: UserRequestAdd = Body(
        openapi_examples={
            "1": Example(
                summary="Anton",
                value={"email": "anton.tihov.94@gmail.com", "password": "qwerty12345678"},
            )
        }
    ),
    response: Response = Response(),
):
    user = await db.users.get_user_with_hashed_password(email=user_data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Неправильный логин или пароль")
    if not AuthService().verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неправильный логин или пароль")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)

    return {"access_token": access_token}


@router.post("/logout", summary="Выход из системы")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}


@router.get("/me")
async def get_me(db: DBDep, user_id: UserIdDep):
    user = await db.users.get_one_or_none(id=user_id)
    return {"data": user}
