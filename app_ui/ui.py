import pprint

from actions.library_actions import Action
from app_orm.ORM import BooksManager
from config import HELLO_MESSAGE, FUNCTIONAL_DESCRIPTION
from utils.search import Search
from validators.add_book_validator import AddBookValidator


class UserInterface:

    def __init__(self):
        self.__books_manager = BooksManager()
        self.__action = Action()

        print(HELLO_MESSAGE, '\n')
        self.request_action()

    def request_action(self):
        print(FUNCTIONAL_DESCRIPTION, '\n')

        action: str = str(input('Что вы хотите сделать? Введите команду: ', )).lower().strip()

        match action:

            case '/add':
                self.add_book()
            case '/all':
                self.all()
            case '/delete':
                self.delete()
            case '/search':
                self.search_book()
            case '/change-status':
                self.change_status()
            case '/exit':
                print("Всего доброго, спасибо за работу!")
            case _:
                print("Команда не распознана, повторите попытку")
                self.request_action()

    def all(self):
        books: dict.values = self.__books_manager.get_all_books().values()
        if books:
            print(*[pprint.pformat(book, sort_dicts=False, indent=4) for book in books], sep='\n')
        else:
            print("В библиотеке нет книг")
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
            self.__books_manager.add_new_book(title, author, year.replace('BC', 'до н.э.'))
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

    def delete(self):
        ids: list[str] = list(map(lambda pk: pk.strip(), input('Введите id тех книг, которые вы хотите удалить. Разделяйте их запятыми: ').split(
                           ',')))
        result = self.__books_manager.delete_books(ids)
        if not result:
            print("Удаление пошло не по плану, обратитесь в технический отдел\n")
        self.request_action()

    def change_status(self):
        book_id = input('Введите id книги, статус которой хотите поменять').strip()
        message, response = self.__action.get_changing_book(book_id)
        if response:
            print(message)
            self.input_status()
        else:
            print(message)
            self.change_status()

    def input_status(self):
        new_status = input('Введите новый статус').strip()
        message, response = self.__action.change_status(new_status)
        if response is True:
            print(message)
            self.request_action()
        else:
            print(message),
            self.input_status()

