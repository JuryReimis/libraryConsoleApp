from app_orm.ORM import BooksManager
from validators.change_status_validator import ChangeStatusValidator


class Action:

    def __init__(self):
        self._book_manager = BooksManager()
        self._books = self._book_manager.get_all_books()
        self._pk: str | None = None

        # Validators:
        self._change_status_validator = ChangeStatusValidator(self._books)

    def get_all_books(self):
        pass

    def get_changing_book(self, pk: str) -> (str, bool):
        pk_error = self._change_status_validator.validate_pk(pk)
        if pk_error:
            return pk_error, False
        else:
            book = self._books.get(pk)
            message = f'{book}'
            self._pk = pk
            return message, True

    def change_status(self, new_status: str) -> (str, bool):
        if self._pk:
            validation_result = self._change_status_validator.validate_status(new_status)
            if validation_result is not None:
                return validation_result, False

            result = self._book_manager.update_status(self._pk, new_status)
            if result is None:
                return "Изменение статуса прошло успешно", True
            return result, False
        else:
            return "Нет данных об id. Обратитесь в технический отдел или попробуйте снова", False

