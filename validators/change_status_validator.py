from validators.base_validator import BaseValidator


class ChangeStatusValidator(BaseValidator):
    r"""Класс для проверок введенного статуса"""

    def __init__(self, books: dict, localization=None):
        super().__init__(localization)
        self._books = books
        self._allowed_statuses = ['в наличии', 'выдана']

    def validate_pk(self, pk) -> str | None:
        r"""Проверяет, доступна ли вообще книга по запрашиваемому id.
        Возвращает ошибку или None
        """
        if pk not in self._books.keys():
            return self._localization.NO_BOOKS_WITH_INPUT_ID_ERROR + pk
        else:
            return None

    def validate_status(self, new_status: str) -> str | None:
        r"""Проверят сам статус на соответствие разрешенным вариантам.
        Возвращает ошибку или None
        """
        if new_status in self._allowed_statuses:
            return None
        return self._localization.NOT_ALLOWED_STATUS_ERROR
