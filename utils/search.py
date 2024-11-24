import re

from app_orm.ORM import BooksManager


class Search:
    r"""Инструмент, написанный для формирования запроса к базе данных по полученным от пользователя данным.
    """

    def __init__(self):
        r"""Инициализация. Формирования экземпляра _books_manager и всех атрибутов, необходимых для работы.
        """
        self._books_manager = BooksManager()
        self._searched_books: [dict] = []
        self._books: [dict] = self._books_manager.get_all_books().values()

        self._default_pattern: re.Pattern | None = None
        self._conjunction_patterns: [re.Pattern] = []

    def init_search(self, values: list) -> None:
        r"""Инициализация поиска.
        В методе происходит обход списка поисковых запросов и формирование списка результатов.
        """
        self._searched_books = []
        self._conjunction_patterns = []
        self._compile_pattern(values)
        if self._conjunction_patterns or self._default_pattern:
            for book in self._books:
                if self._search_in_book(self._default_pattern, book):
                    self._searched_books.append(book)
                else:
                    for patterns in self._conjunction_patterns:
                        if self._exact_search(patterns, book):
                            self._searched_books.append(book)

    def get_searched_books(self) -> list:
        return self._searched_books

    @staticmethod
    def _search_in_book(pattern: re.Pattern, book: dict) -> None | re.Match:
        r"""Метод сравнивает поля книги с паттерном, возвращает None если совпадения нет.
        """
        if not pattern:
            return None
        result = None
        title = book.get('title')
        author = book.get('author')
        year = str(book.get('year'))
        for string in title, author, year:
            if result:
                return result
            result = pattern.search(string)
        return result

    def _exact_search(self, patterns: list, book: dict) -> bool:
        r"""Подробный поиск или точный поиск. Обходит по всем паттернам и если хотя бы с одним нет совпадения -
        возвращает False. Иначе True.
        """
        for pattern in patterns:
            if self._search_in_book(pattern, book):
                continue
            else:
                return False
        return True

    def _compile_pattern(self, values: list) -> None:
        r"""Компиляция регулярного выражения для каждого поискового запроса и отделение обычных запросов от точных.
        """
        escaped_strings = []
        for string in values:
            string = self.replace_local_abbreviation(string)
            conjunction_request = string.split('&&&')
            if len(conjunction_request) > 1:
                self._compile_conjunction_pattern(conjunction_request)
            else:
                escaped_strings.append(re.escape(string))
        if escaped_strings:
            self._default_pattern = re.compile('|'.join(escaped_strings), re.IGNORECASE)
        else:
            self._default_pattern = None

    def _compile_conjunction_pattern(self, strings: list) -> None:
        r"""Компиляция регулярных выражений для точных поисковых запросов
        """
        patterns = [re.compile(re.escape(string), re.IGNORECASE) for string in strings]
        self._conjunction_patterns.append(patterns)

    @staticmethod
    def replace_local_abbreviation(string: str, pattern: str = r'(\d+)\s*(BC)', local_ab: str = 'BC') -> str:
        r"""Метод для единообразного сохранения даты в базе данных.
        Происходит замена локальных аббревиатур на стандартную русскую"""
        result = re.search(pattern, string)
        if result:
            return string.replace(local_ab, 'до н.э.')
        else:
            return string
