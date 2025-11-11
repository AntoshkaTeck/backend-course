from datetime import date

from fastapi import HTTPException


class ExceptionBase(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(ExceptionBase):
    detail = "Объект не найден"


class HotelNotFoundException(ExceptionBase):
    detail = "Отель не найден"


class RoomNotFoundException(ExceptionBase):
    detail = "Номер не найден"


class UserNotFoundException(ExceptionBase):
    detail = "Пользователь не найден"


class IncorrectPasswordException(ExceptionBase):
    detail = "Неправильный email или пароль"


class AllRoomsAreBookedException(ExceptionBase):
    detail = "Не осталось свободных номеров"


class ObjectAlreadyExistsException(ExceptionBase):
    detail = "Объект уже существует"


class UserAlreadyExistsException(ExceptionBase):
    detail = "Пользователь уже существует"


class IncorrectDatesException(ExceptionBase):
    detail = "Дата выезда не может быть раньше или равна дате заезда"


class InvalidTokenException(ExceptionBase):
    detail = "Ошибка в токене"


def validate_booking_dates(date_from: date, date_to: date):
    if date_to <= date_from:
        raise IncorrectDatesException


class HTTPExceptionBase(HTTPException):
    detail = None
    status_code = 500

    def __init__(self):
        super().__init__(self.status_code, self.detail)


class HotelNotFoundHTTPException(HTTPExceptionBase):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(HTTPExceptionBase):
    status_code = 404
    detail = "Номер не найден"


class AllRoomsAreBookedHTTPException(HTTPExceptionBase):
    detail = "Не осталось свободных номеров"
    status_code = 409


class UserAlreadyExistsHTTPException(HTTPExceptionBase):
    detail = "Пользователь с таким email существует"
    status_code = 409


class IncorrectPasswordHTTPException(HTTPExceptionBase):
    detail = "Неправильный email или пароль"
    status_code = 401


class InvalidTokenHTTPException(HTTPExceptionBase):
    detail = "Ошибка в токене"
    status_code = 401


class NoAccessTokenHTTPException(HTTPExceptionBase):
    detail = "Вы не предоставили токен доступа"
    status_code = 401
