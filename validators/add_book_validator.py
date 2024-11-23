import re
from string import digits

from utils.search import Search


class AddBookValidator:

    def __init__(self, title: str = None, author: str = None, year: str = None):
        self._title = title
        self._author = author
        self._year = year

    def validate_title(self, title) -> str | None:
        self._title = title
        search = Search()
        search.init_search([title])
        searched_books = search.get_searched_books()
        if searched_books:
            return "Уже есть книги с таким названием, проверьте, хотите ли вы продолжить"
        else:
            return None

    def validate(self, author: str) -> None | str:
        self._author = author
        search = Search()
        search.init_search(['&&&'.join((self._title, self._author, self._year))])
        searched_books = search.get_searched_books()
        if searched_books:
            return (f"""!!!Вы пытаетесь добавить книгу, которая уже есть в базе данных 
Название: {searched_books[0].get('title')}
Автор: {searched_books[0].get('author')}
Год издания: {searched_books[0].get('year')}
Если здесь есть какая-то ошибка - обратитесь в технический отдел или воспользуйтесь \"Жестким\" добавлением\n""")
        return None

    def validate_year(self, year: str, bc_pattern: str = r'(\d+)\s*(д\.н\.э\.|до н\.э\.|BC)?(.*)') -> None | str:
        self._year = year
        error = 'В значении "Год" Присутствует неизвестный символ, который не является цифрой'
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

