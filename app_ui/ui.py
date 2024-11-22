import pprint

from app_orm.ORM import BooksManager
from config import HELLO_MESSAGE, FUNCTIONAL_DESCRIPTION
from utils.search import Search
from validators.add_book_validator import AddBookValidator


class UserInterface:

    def __init__(self):

        print(HELLO_MESSAGE, '\n')
        self.request_action()

    def request_action(self):
        print(FUNCTIONAL_DESCRIPTION, '\n')

        action: str = str(input('Что вы хотите сделать? Введите команду: ',)).lower()

        match action:

            case '/add':
                self.add_book()
            case '/all':
                books = BooksManager().get_all_books()
                if books:
                    print(*[pprint.pformat(book, sort_dicts=False, indent=4) for book in books], sep='\n')
                else:
                    print("В библиотеке нет книг")
                self.request_action()
            case '/delete':
                print("Удалить книгу")
            case '/search':
                self.search_book()
            case '/change-status':
                print("Сменить статус книги")
            case '/exit':
                print("Всего доброго, спасибо за работу!")
            case _:
                print("Команда не распознана, повторите попытку")
                self.request_action()

    def add_book(self):
        print("Для добавления книги последовательно введите название, автора и год издания")
        title = str(input('Введите название книги: '))
        search = Search()
        search.init_search([title])
        print('Здесь предупреждение, что книга с таким названием уже имеется', search.get_searched_books())
        author = str(input('Введите автора книги: '))
        year = str(input('Введите год издания: '))
        validation = AddBookValidator(title, author, year)
        errors = validation.validate()

        if not errors:
            BooksManager().add_new_book(title, author, year)
        else:
            print('Произошла ошибка при добавлении книги в базу данных', *errors, sep='\n')
        self.request_action()

    def search_book(self):
        print(r"""Введите название книги, автора или год издания.
         Можете указать несколько значений, разделяя их `;` для глобального поиска
         Например: Мартин; 1980; Хроники Войны; Прокопий""")
        strings = input("Что ищем: ").split(';')
        search = Search()
        search.init_search(strings)
        print(search.get_searched_books())
        self.request_action()


