from app_orm.ORM import BooksManager
from config import LIBRARY_HEADERS
from utils.colouring import ConsoleColors
from utils.pretty_tables import PrettyTables
from utils.search import Search
from validators.add_book_validator import AddBookValidator
from validators.change_status_validator import ChangeStatusValidator


class Action:
    r"""Базовый класс действий. Здесь формируется атрибут класса _books_manager для взаимодействия с бд
    При этом далее все наследующиеся от данного классы получают равный доступ к данным, хранящимся в
    _books_manager
    """

    _books_manager = BooksManager()
    _localization = None
    _library_headers = LIBRARY_HEADERS

    def __init__(self, localization=None):
        self.set_localization(localization)

    def set_localization(self, localization):
        r"""Установка констант локализации
        """
        if localization:
            self._localization = localization
        else:
            from localizations.loc_RU import LocalizationConstants
            self._localization = LocalizationConstants
        self._books_manager.set_localization(self._localization)

    def get_all_books(self) -> (str, bool):
        r"""Метод для получения списка всех книг из базы данных библиотеки.
        Формирует строку для вывода в консоль. Возвращает строку и bool значение, является ли результат ожидаемым
        или произошла какая-то ошибка.
        """
        try:
            books = self._books_manager.get_all_books()
            if books:
                pretty_table = PrettyTables(headers=LIBRARY_HEADERS, table_data=books.values())
                return pretty_table.get_pretty_table(), True
            else:
                return ConsoleColors.colour_text(self._localization.EMPTY_LIBRARY_WARNING, 'WHITE'), True
        except Exception as error:
            return f'{self._localization.JUST_ERROR}\n{error}', False


class AddBookAction(Action):
    r"""Класс действия, сосредоточенный на обработке данных для добавления новой книги в бд"""

    def __init__(self, localization=None):
        super().__init__(localization)
        self._title = None
        self._validator = AddBookValidator(self._localization)

    def input_title(self, title: str) -> (str, bool):
        r"""Метод принимает введенное название книги и валидирует его.
        Возвращает кортеж из строки и bool значения, которое определяет были ли получены каки-то ошибки
        """
        self._title = title
        validation_error = self._validator.validate_title(title)
        if validation_error is None:
            return '', True
        else:
            return validation_error, False

    def add_book(self, author: str, year: str) -> (str, bool):
        r"""Метод получает оставшиеся данные о новой книге, проверяет их.
        Возвращает либо сообщение об успешном добавлении с True, либо ошибку с False
        """
        year_error = self._validator.validate_year(year)
        if year_error is not None:
            return year_error, False
        error = self._validator.validate(author)
        if error:
            return error, False
        year = self._validator.transform_year()
        self._books_manager.add_new_book(self._title, author, year)
        return self._localization.ADD_BOOK_SUCCESS, True


class SearchBooksAction(Action):
    r"""Класс, нацеленный на обработку действий по поиску книги в библиотеке.
    """

    def __init__(self, query: str, localization=None):
        super().__init__(localization)
        self._split_query: list = list(map(lambda q: q.strip(), query.split(';')))

    def search(self) -> (str, bool):
        r"""Метод для инициализации поиска и возврата результатов этого поиска
        """
        search = Search()
        search.init_search(self._split_query)
        searched_books = search.get_searched_books()
        if searched_books:
            pretty_table = PrettyTables(LIBRARY_HEADERS, searched_books)
            return pretty_table.get_pretty_table(), True
        return self._localization.NO_BOOKS_WARNING, False


class DeleteBooksByIdAction(Action):
    r"""Класс, направленный на обработку действий по удалению книг из бд
    """

    def __init__(self, ids_string: str, localization=None):
        super().__init__(localization)
        self._ids: list[str] = list(map(lambda pk: pk.strip(), ids_string.split(
            ',')))  # Происходит формирование списка запросов, по которым будет произведен поиск

    def delete(self) -> (str, bool):
        r"""Метод направлен на запрос удаления по сформированному списку и возврат сообщения или ошибки.
        По аналогии с предыдущими действиями возврат идет в форме кортежа, где нулевой элемент является сообщением,
        а первый ool значением, харрактеризующим успешность операции.
        """
        result = self._books_manager.delete_books(self._ids)
        if isinstance(result, tuple):
            deleted_books, not_exist_books = result[0], result[1]
            if deleted_books:
                pretty_table = PrettyTables(LIBRARY_HEADERS, deleted_books)
                message = f'{ConsoleColors.colour_text(
                    self._localization.DELETE_BOOKS_SUCCESS, 'MAGENTA')}:\n{pretty_table.get_pretty_table()}\n'
            else:
                message = ''
            for book in not_exist_books:
                message += f'{ConsoleColors.colour_text(book, 'RED')}\n'
            return message, True
        else:
            return self._localization.DELETE_BOOKS_ERROR, False


class ChangeStatusAction(Action):
    r"""Класс, направленный на обработку действий, связанных с изменением статуса книги в библиотеке
    """

    def __init__(self, pk: str, localization=None):
        super().__init__(localization)
        self._change_status_validator = ChangeStatusValidator(self._books_manager.get_all_books())
        self._pk = pk

    def get_changing_book(self) -> (str, bool):
        r"""Метод, нацеленный на обработку введенного id
        """
        pk_error = self._change_status_validator.validate_pk(self._pk)
        if pk_error:
            return ConsoleColors.colour_text(pk_error, 'RED'), False
        else:
            book = self._books_manager.get_all_books().get(self._pk)
            pretty_table = PrettyTables(LIBRARY_HEADERS, [book])
            message = pretty_table.get_pretty_table()
            return ConsoleColors.colour_text(message, 'MAGENTA'), True

    def change_status(self, new_status: str) -> (str, bool):
        r"""Метод, нацеленный на обработку введенного пользователем статуса"""
        if self._pk:
            validation_result = self._change_status_validator.validate_status(new_status)
            if validation_result is not None:
                return validation_result, False

            result = self._books_manager.update_status(self._pk, new_status)
            if result is None:
                return ConsoleColors.colour_text(
                    self._localization.CHANGING_STATUS_SUCCESS, 'MAGENTA'), True
            return result, False
        else:
            return self._localization.CHANGING_STATUS_NO_ID_ERROR, False
