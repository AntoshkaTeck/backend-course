from datetime import date

from fastapi import HTTPException


class ExceptionBase(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(ExceptionBase):
    detail = "Объект не найден"


class AllRoomsAreBookedException(ExceptionBase):
    detail = "Не осталось свободных номеров"


class ObjectAlreadyExistsException(ExceptionBase):
    detail = "Объект уже существует"


class IncorrectDatesException(ExceptionBase):
    detail = "Дата выезда не может быть раньше или равна дате заезда"


def validate_booking_dates(date_from: date, date_to: date):
    if date_to <= date_from:
        raise IncorrectDatesException


class HTTPExceptionBase(HTTPException):
    detail = None
    status_code = 500

    def __init__(self):
        super().__init__(self.status_code, self.detail)


class HotelNotFoundException(HTTPExceptionBase):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundException(HTTPExceptionBase):
    status_code = 404
    detail = "Номер не найден"
