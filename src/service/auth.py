from datetime import datetime, timezone, timedelta

from pwdlib import PasswordHash
import jwt
from pydantic import EmailStr

from src.config import settings
from src.exceptions import (
    ObjectAlreadyExistsException,
    UserAlreadyExistsException,
    InvalidTokenException,
    ObjectNotFoundException,
    UserNotFoundException,
    IncorrectPasswordException,
    ExpiredTokenException,
)
from src.schemas.users import UserRequestAdd, UserAdd, User, UserWithHashedPassword
from src.service.base import BaseService


class AuthService(BaseService):
    password_hash = PasswordHash.recommended()

    def verify_password(self, plain_password, hashed_password) -> bool:
        return self.password_hash.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.password_hash.hash(password)

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.exceptions.InvalidSignatureError:
            raise InvalidTokenException
        except jwt.exceptions.ExpiredSignatureError:
            raise ExpiredTokenException

    async def register_user(self, user_data: UserRequestAdd) -> None:
        hashed_password = self.hash_password(user_data.password)
        new_user_data = UserAdd(email=user_data.email, hashed_password=hashed_password)
        try:
            await self.db.users.add(new_user_data)
            await self.db.commit()
        except ObjectAlreadyExistsException as ex:
            raise UserAlreadyExistsException from ex

    async def login_user(self, user_data: UserRequestAdd) -> str:
        user = await self.get_user_with_hash_pass_and_check(email=user_data.email)
        if not self.verify_password(user_data.password, user.hashed_password):
            raise IncorrectPasswordException
        return self.create_access_token({"user_id": user.id})

    async def get_user_with_hash_pass_and_check(self, email: EmailStr) -> UserWithHashedPassword:
        try:
            return await self.db.users.get_user_with_hashed_password(email=email)
        except ObjectNotFoundException:
            raise UserNotFoundException

    async def get_me(self, user_id: int) -> User:
        return await self.get_user_by_id(user_id=user_id)

    async def get_user_by_id(self, user_id: int) -> User:
        try:
            return await self.db.users.get_one(id=user_id)
        except ObjectNotFoundException:
            raise UserNotFoundException
