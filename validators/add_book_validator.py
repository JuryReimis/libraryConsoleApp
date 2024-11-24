import re
from string import digits

from config import LIBRARY_HEADERS
from utils.colouring import ConsoleColors
from utils.pretty_tables import PrettyTables
from utils.search import Search
from validators.base_validator import BaseValidator


class AddBookValidator(BaseValidator):
    r"""Класс для проверки корректности данных при добавлении новой книги
    """

    def __init__(self, title: str = None, author: str = None, year: str = None, localization=None):
        super().__init__(localization)
        self._title = title
        self._author = author
        self._year = year

    def validate_title(self, title) -> str | None:
        r"""Проверка, существует ли книга с представленным названием в базе данных.
        Возвращает Ошибку или None
        """
        self._title = title
        search = Search()
        search.init_search([title])
        searched_books = search.get_searched_books()
        if searched_books:
            pretty_table = PrettyTables(LIBRARY_HEADERS, searched_books)
            return f"{ConsoleColors.colour_text(
                self._localization.EXIST_TITLE_WARNING, 'WHITE')}{pretty_table.get_pretty_table(
                )}"
        else:
            return None

    def validate(self, author: str) -> None | str:
        r"""Метод проверяет все данные вместе. Возвращает ошибку или None
        """
        self._author = author
        search = Search()
        search.init_search(['&&&'.join((self._title, self._author, self._year))])
        searched_books = search.get_searched_books()
        if searched_books:
            pretty_table = PrettyTables(LIBRARY_HEADERS, searched_books)
            return f"{ConsoleColors.colour_text(
                self._localization.EXIST_BOOK_ERROR, 'RED')}{pretty_table.get_pretty_table()}"
        return None

    def validate_year(self, year: str, bc_pattern: str = r'(\d+)?\s*(д\.н\.э\.|до н\.э\.|BC)?(.*)') -> None | str:
        r"""Метод проверяет корректность введенного года.
        Возвращает ошибку или None
        """
        self._year = year
        error = self._localization.NO_DIGIT_IN_YEAR
        if year == "Неизвестно":
            return None
        bc = re.search(bc_pattern, year)
        if bc.group(3):
            return error
        for char in bc.group(1):
            if char not in digits:
                return error
        return None

    def transform_year(self, source: str = 'EN', target: str = 'RU') -> str:
        return self._year.replace('BC', 'до н.э.')
