class ChangeStatusValidator:

    def __init__(self, books: dict):
        self._books = books
        self._allowed_statuses = ['в наличии', 'выдана']

    def validate_pk(self, pk) -> str | None:
        if pk not in self._books.keys():
            return "В базе данных нет книг с указанным id: " + pk
        else:
            return None

    def validate_status(self, new_status: str):
        if new_status in self._allowed_statuses:
            return None
        return "Введенный статус не является разрешенным, повторите попытку"
