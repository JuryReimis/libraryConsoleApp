from actions.library_actions import Action, ChangeStatusAction, AddBookAction, SearchBooksAction, DeleteBooksByIdAction
from config import HELLO_MESSAGE, FUNCTIONAL_DESCRIPTION


class UserInterface:

    def __init__(self, localization: str = "RU"):

        # Actions:
        self.__action = Action()
        self.__add_book_action = None
        self.__search_book_action = None
        self.__delete_book_action = None
        self.__change_status_action = None

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
                print("\nВсего доброго, спасибо за работу!\n")
            case _:
                print("\nКоманда не распознана, повторите попытку\n")
                self.request_action()

    def all(self):
        message, response = Action().get_all_books()
        print(message)
        self.request_action()

    def add_book(self):
        self.__add_book_action = AddBookAction()
        print()
        print("Для добавления книги последовательно введите название, автора и год издания")
        title = str(input('Введите название книги: '))
        message, response = self.__add_book_action.input_title(title)
        if response is False:
            print(message)
        author = str(input('Введите автора книги: '))
        year = str(input('Введите год издания: '))
        message, response = self.__add_book_action.add_book(author, year)
        print(message)
        self.request_action()

    def search_book(self):
        print("""\nВведите название книги, автора или год издания.
         Можете указать несколько значений, разделяя их `;` для глобального поиска
         Например: Мартин; 1980; Хроники Войны; Прокопий""")
        query = input("Что ищем: ")
        self.__search_book_action = SearchBooksAction(query)
        message, response = self.__search_book_action.search()
        print(message)
        self.request_action()

    def delete(self):
        print()
        ids: str = input('Введите id тех книг, которые вы хотите удалить. Разделяйте их запятыми: ')
        self.__delete_book_action = DeleteBooksByIdAction(ids)
        message, response = self.__delete_book_action.delete()
        print(message)
        self.request_action()

    def change_status(self):
        print()
        book_id = input('Введите id книги, статус которой хотите поменять: ').strip()
        self.__change_status_action = ChangeStatusAction(book_id)
        message, response = self.__change_status_action.get_changing_book()
        if response:
            print(message)
            self.input_status()
        else:
            print(message)
            self.change_status()

    def input_status(self):
        print()
        new_status = input('Введите новый статус: ').strip().lower()
        message, response = self.__change_status_action.change_status(new_status)
        if response is True:
            print(message)
            self.request_action()
        else:
            print(message)
            self.input_status()
