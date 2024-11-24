from actions.library_actions import Action, ChangeStatusAction, AddBookAction, SearchBooksAction, DeleteBooksByIdAction
from config import INIT_MESSAGE, SUPPORTED_LANGUAGES, WRONG_LANGUAGE
from utils.colouring import ConsoleColors


class UserInterface:
    r""" Класс интерфейса пользователя. Его экземпляр дает возможность взаимодействия с программой через консоль.
    В нем происходит ТОЛЬКО взаимодействие с пользователем и вывод в консоль полученных, в ходе работы программы
    данных.
    """

    def __init__(self):
        r"""Инициализация базовых атрибутов экземпляра. Инициализация перевода на доступные языки.
        При невозможности получить файл с константами перевода приложение закрывается.
        """

        # Actions:
        self.__action = Action()
        self.__add_book_action = None
        self.__search_book_action = None
        self.__delete_book_action = None
        self.__change_status_action = None

        self.localization = None

        self.init_language()

        if self.localization:
            print(ConsoleColors.colour_text(self.localization.HELLO_MESSAGE, 'GREEN'), '\n')
            self.request_action()
        else:
            print()

    def init_language(self):
        r"""Инициализация констант локализации
        """

        language = input(ConsoleColors.colour_text(INIT_MESSAGE, 'CYAN')).strip().upper()

        if language not in SUPPORTED_LANGUAGES:
            print(ConsoleColors.colour_text(WRONG_LANGUAGE, 'RED'))
            self.init_language()
        else:
            match language:
                case 'RU':
                    from localizations.loc_RU import LocalizationConstants
                    self.localization = LocalizationConstants
                case 'EN':
                    from localizations.loc_EN import LocalizationConstants
                    self.localization = LocalizationConstants

    def request_action(self):
        r"""Запрос команды на совершение действия.
        После получения команды происходит перенаправление на соответствующий метод.
        """

        print(ConsoleColors.colour_text(self.localization.FUNCTIONAL_DESCRIPTION, 'blue'), '\n')

        action: str = str(
            input(ConsoleColors.colour_text(self.localization.ACTION_REQUEST, 'GREEN'), )).lower().strip()

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
                print(ConsoleColors.colour_bright_text(self.localization.GOODBYE_MESSAGE, 'GREEN'))
            case _:
                print(ConsoleColors.colour_text(self.localization.REPEAT_COMMAND, 'RED'))
                self.request_action()

    def all(self):
        r"""Метод, служащий для вывода всей библиотеки в консоль
        """
        message, response = Action(self.localization).get_all_books()
        if response is True:
            print(message)
        else:
            print(ConsoleColors.colour_text(message, 'RED'))
        self.request_action()

    def add_book(self):
        r"""Метод, служащий для сбора с пользователя данных, на основе которых будет добавлена новая книга.
        """
        self.__add_book_action = AddBookAction(self.localization)
        print()
        print(ConsoleColors.colour_bright_text(
            self.localization.ADD_BOOK_INFO_MESSAGE, 'GREEN'))
        title = str(input(ConsoleColors.colour_text(self.localization.INPUT_TITLE_MESSAGE, 'YELLOW')))
        message, response = self.__add_book_action.input_title(title)
        if response is False:
            print(message)
        author = str(input(ConsoleColors.colour_text(self.localization.INPUT_AUTHOR_MESSAGE, 'YELLOW')))
        year = str(input(ConsoleColors.colour_text(self.localization.INPUT_YEAR_MESSAGE, 'YELLOW')))
        message, response = self.__add_book_action.add_book(author, year)
        print(ConsoleColors.colour_bright_text(message, 'MAGENTA'))
        self.request_action()

    def search_book(self):
        r"""Метод, служащий для сбора с пользователя данных, на основе которых будет произведен поиск.
        """
        print(ConsoleColors.colour_bright_text(self.localization.SEARCH_INFO_MESSAGE, 'GREEN'))
        query = input(ConsoleColors.colour_text(self.localization.INPUT_QUERY_MESSAGE, 'YELLOW'))
        self.__search_book_action = SearchBooksAction(query, self.localization)
        message, response = self.__search_book_action.search()
        if response is True:
            print(message)
        else:
            print(ConsoleColors.colour_text(message, 'WHITE'))
        self.request_action()

    def delete(self):
        r"""Метод, служащий для сбора с пользователя данных, на основе которых будет произведено удаление книг.
        """
        print()
        ids: str = input(ConsoleColors.colour_text(
            self.localization.INPUT_DELETE_IDS_MESSAGE, 'YELLOW'))
        self.__delete_book_action = DeleteBooksByIdAction(ids, self.localization)
        message, response = self.__delete_book_action.delete()
        if response is True:
            print(message)
        else:
            print(ConsoleColors.colour_text(message, 'RED'))
        self.request_action()

    def change_status(self):
        r"""Метод, служащий для сбора с пользователя данных о том, статус какой книги необходимо изменить
        """
        print()
        book_id = input(ConsoleColors.colour_text(
            self.localization.INPUT_CHANGING_BOOK_ID_MESSAGE, 'YELLOW')).strip()
        self.__change_status_action = ChangeStatusAction(book_id, self.localization)
        message, response = self.__change_status_action.get_changing_book()
        if response:
            print(message)
            self.input_status()
        else:
            print(message)
            self.change_status()

    def input_status(self):
        r"""Метод, расширяющий взаимодействие с пользователем на предмет изменения статуса.
        Собирает данные, на основе которых формируется новый статус книги"""
        print()
        new_status = input(
            ConsoleColors.colour_text(self.localization.INPUT_NEW_STATUS_MESSAGE, 'YELLOW')).strip().lower()
        message, response = self.__change_status_action.change_status(new_status)
        if response is True:
            print(message)
            self.request_action()
        else:
            print(ConsoleColors.colour_text(message, 'RED'))
            self.input_status()
