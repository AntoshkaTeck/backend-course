from datetime import date

from fastapi import HTTPException


class ExceptionBase(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self):
        super().__init__(self.detail)


class ObjectNotFoundException(ExceptionBase):
    detail = "Объект не найден"


class HotelNotFoundException(ExceptionBase):
    detail = "Отель не найден"


class RoomNotFoundException(ExceptionBase):
    detail = "Номер не найден"

class FacilityNotFoundException(ExceptionBase):
    detail = "Удобство не найдено"


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

class InvalidBookingDatesException(ExceptionBase):
    detail = "Дата бронирования не может быть раньше текущей даты"


class InvalidTokenException(ExceptionBase):
    detail = "Ошибка в токене"

class ExpiredTokenException(ExceptionBase):
    detail = "Срок действия токена истек"


class ObjectEmptyFieldsException(ExceptionBase):
    detail = "Не передано ни одного поля для изменения объекта"

class ObjectLinkNotFoundException(ExceptionBase):
    detail = "Объект для связи с другим объектом не найдено"

class RoomFacilityNotFoundException(ExceptionBase):
    detail = "Удобство для связи с номером не найдено"


class HotelEmptyFieldsException(ExceptionBase):
    detail = "Не передано ни одного поля для изменения отеля"

class RoomEmptyFieldsException(ExceptionBase):
    detail = "Не передано ни одного поля для изменения номера"


def validate_booking_dates(date_from: date, date_to: date):
    today = date.today()
    if date_to < today or date_from < today:
        raise InvalidBookingDatesException

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

class FacilityNotFoundHTTPException(HTTPExceptionBase):
    status_code = 404
    detail = "Удобство не найдено"

class RoomFacilityNotFoundHTTPException(HTTPExceptionBase):
    status_code = 409
    detail = "Удобство для связи с номером не найдено"


class HotelEmptyFieldsHTTPException(HTTPExceptionBase):
    status_code = 422
    detail = "Не передано ни одного поля для изменения отеля"


class RoomEmptyFieldsHTTPException(HTTPExceptionBase):
    status_code = 422
    detail = "Не передано ни одного поля для изменения номера"


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

class InvalidBookingDatesHTTPException(HTTPExceptionBase):
    detail = "Дата бронирования не может быть раньше текущей даты"
    status_code = 422

class IncorrectDatesHTTPException(HTTPExceptionBase):
    detail = "Дата выезда не может быть раньше или равна дате заезда"
    status_code = 422

class ExpiredTokenHTTPException(HTTPExceptionBase):
    detail = "Срок действия токена истек"
    status_code = 403