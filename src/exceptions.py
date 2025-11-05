class ExceptionBase(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(ExceptionBase):
    detail = "Объект не найден"


class AllRoomsAreBookedException(ExceptionBase):
    detail = "Не осталось свободных номеров"


class UserAlreadyExistException(ExceptionBase):
    detail = "Пользователь с таким e-mail уже существует"


class IncorrectDatesException(ExceptionBase):
    detail = "Дата выезда не может быть раньше или равна дате заезда"
