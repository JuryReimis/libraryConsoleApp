import re

from app_orm.ORM import BooksManager


class Search:

    def __init__(self):
        self._books_manager = BooksManager()
        self._searched_books: [dict] = []
        self._books: [dict] = self._books_manager.get_all_books()

        self._default_pattern: re.Pattern | None = None
        self._conjunction_patterns: [re.Pattern] = []

    def init_search(self, values: list) -> None:
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
        for pattern in patterns:
            if self._search_in_book(pattern, book):
                continue
            else:
                return False
        return True

    def _compile_pattern(self, values: list) -> None:
        escaped_strings = []
        for string in values:
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
        patterns = [re.compile(re.escape(string)) for string in strings]
        self._conjunction_patterns.append(patterns)
