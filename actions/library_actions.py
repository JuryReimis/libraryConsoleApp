import pprint

from app_orm.ORM import BooksManager
from validators.change_status_validator import ChangeStatusValidator


class Action:

    def __init__(self):
        self._book_manager = BooksManager()
        self._pk: str | None = None

        # Validators:
        self._change_status_validator = ChangeStatusValidator(self._book_manager.get_all_books())

    def get_all_books(self) -> (str, bool):
        try:
            books = self._book_manager.get_all_books()
            if books:
                return f'{[pprint.pformat(book, sort_dicts=False, indent=4) for book in books.values()]}', True
            else:
                return "В библиотеке нет книг", True
        except Exception as error:
            return f'Произошла ошибка при обращении к базе данных, обратитесь в технический отдел или повторите попытку\n{error}', False

    def get_changing_book(self, pk: str) -> (str, bool):
        pk_error = self._change_status_validator.validate_pk(pk)
        if pk_error:
            return pk_error, False
        else:
            book = self._book_manager.get_all_books().get(pk)
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
