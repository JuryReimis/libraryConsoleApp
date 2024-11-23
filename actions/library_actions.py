
from app_orm.ORM import BooksManager
from config import LIBRARY_HEADERS
from utils.pretty_tables import PrettyTables
from utils.search import Search
from validators.add_book_validator import AddBookValidator
from validators.change_status_validator import ChangeStatusValidator


class Action:
    _books_manager = BooksManager()

    def get_all_books(self) -> (str, bool):
        try:
            books = self._books_manager.get_all_books()
            if books:
                pretty_table = PrettyTables(headers=LIBRARY_HEADERS, table_data=books.values())
                return pretty_table.get_pretty_table(), True
            else:
                return "В библиотеке нет книг", True
        except Exception as error:
            return f'Произошла ошибка при обращении к базе данных, обратитесь в технический отдел или повторите попытку\n{error}', False


class AddBookAction(Action):

    def __init__(self):
        self._title = None
        self._validator = AddBookValidator()

    def input_title(self, title: str) -> (str, bool):
        self._title = title
        validation_error = self._validator.validate_title(title)
        if validation_error is None:
            return '', True
        else:
            return validation_error, False

    def add_book(self, author: str, year: str) -> (str, bool):
        year_error = self._validator.validate_year(year)
        if year_error is not None:
            return year_error, False
        error = self._validator.validate(author)
        if error:
            return error, False
        year = self._validator.transform_year()
        self._books_manager.add_new_book(self._title, author, year)
        return "Книга успешно добавлена!", True


class SearchBooksAction(Action):

    def __init__(self, query: str):
        self._split_query: list = query.split(';')

    def search(self) -> (str, bool):
        search = Search()
        search.init_search(self._split_query)
        searched_books = search.get_searched_books()
        if searched_books:
            pretty_table = PrettyTables(LIBRARY_HEADERS, searched_books)
            return pretty_table.get_pretty_table(), True
        return "Не найдено ни одной книги по вашему запросу", False


class DeleteBooksByIdAction(Action):

    def __init__(self, ids_string: str):
        self._ids: list[str] = list(map(lambda pk: pk.strip(), ids_string.split(
            ',')))

    def delete(self) -> (str, bool):
        result = self._books_manager.delete_books(self._ids)
        if isinstance(result, tuple):
            deleted_books, not_exist_books = result[0], result[1]
            if deleted_books:
                pretty_table = PrettyTables(LIBRARY_HEADERS, deleted_books)
                message = f'Успешно удалены:\n {pretty_table.get_pretty_table()}\n'
            else:
                message = ''
            for book in not_exist_books:
                message += f'{book}\n'
            return message, True
        else:
            return "Возникла проблема с удалением", False


class ChangeStatusAction(Action):

    def __init__(self, pk: str):
        self._change_status_validator = ChangeStatusValidator(self._books_manager.get_all_books())
        self._pk = pk

    def get_changing_book(self) -> (str, bool):
        pk_error = self._change_status_validator.validate_pk(self._pk)
        if pk_error:
            return pk_error, False
        else:
            book = self._books_manager.get_all_books().get(self._pk)
            pretty_table = PrettyTables(LIBRARY_HEADERS, [book])
            message = pretty_table.get_pretty_table()
            return message, True

    def change_status(self, new_status: str) -> (str, bool):
        if self._pk:
            validation_result = self._change_status_validator.validate_status(new_status)
            if validation_result is not None:
                return validation_result, False

            result = self._books_manager.update_status(self._pk, new_status)
            if result is None:
                return "Изменение статуса прошло успешно", True
            return result, False
        else:
            return "Нет данных об id. Обратитесь в технический отдел или попробуйте снова", False
