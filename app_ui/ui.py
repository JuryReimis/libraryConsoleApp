from config import HELLO_MESSAGE, FUNCTIONAL_DESCRIPTION
from utils.search import Search


class UserInterface:

    def __init__(self):

        print(HELLO_MESSAGE, '\n')
        self.request_action()

    def request_action(self):
        print(FUNCTIONAL_DESCRIPTION, '\n')

        action: str = str(input('Что вы хотите сделать? Введите команду: ',)).lower()

        match action:

            case '/add':
                print("Добавление книги")
            case '/all':
                print("Показать список всех книг")
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
        author = str(input('Введите автора книги: '))
        year = int(input('Введите год издания: '))

    def search_book(self):
        print(r"""Введите название книги, автора или год издания.
         Можете указать несколько значений, разделяя их `;` для глобального поиска
         Например: Мартин; 1980; Хроники Войны; Прокопий""")
        strings = input("Что ищем: ").split(';')
        search = Search()
        search.init_search(strings)
        print(search.get_searched_books())
        self.request_action()


