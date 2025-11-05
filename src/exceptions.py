class ExceptionBase(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(ExceptionBase):
    detail = "Объект не найден"


class AllRoomsAreBookedException(ExceptionBase):
    detail = "Не осталось свободных номеров"
