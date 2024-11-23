import re
from string import digits

from utils.search import Search


class AddBookValidator:

    def __init__(self, title: str, author: str, year: str):
        self.title = title
        self.author = author
        self.year = year

    def validate(self) -> list[str]:
        errors = []
        year_errors = self.validate_year()
        if year_errors:
            errors.append(year_errors)
        book_errors = self.validate_book()
        if book_errors:
            errors.append(book_errors)
        return errors

    def validate_year(self, bc_pattern: str = r'(\d+)\s*(д\.н\.э\.|до н\.э\.|BC)?(.*)') -> None | str:
        error = 'В значении "Год" Присутствует неизвестный символ, который не является цифрой'
        if self.year == "Неизвестно":
            return None
        bc = re.match(bc_pattern, self.year)
        if bc.group(3):
            return error

        for char in bc.group(1):
            if char not in digits:
                return error
        return None

    def validate_book(self) -> None | str:
        search = Search()
        search.init_search(["&&&".join((self.title, self.author, self.year))])
        searched_books: list[dict] = search.get_searched_books()
        if searched_books:
            return (f"""!!!Вы пытаетесь добавить книгу, которая уже есть в базе данных 
Название: {searched_books[0].get('title')}
Автор: {searched_books[0].get('author')}
Год издания: {searched_books[0].get('year')}"
Если здесь есть какая-то ошибка - обратитесь в технический отдел или воспользуйтесь \"Жестким\" добавлением\n""")
        return None
