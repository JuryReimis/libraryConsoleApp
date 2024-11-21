from config import HELLO_MESSAGE, FUNCTIONAL_DESCRIPTION


class UserInterface:

    def __init__(self):

        print(HELLO_MESSAGE, '\n')
        self.request_action()

    def request_action(self):
        print(FUNCTIONAL_DESCRIPTION, '\n')

        action: str = str(input('Что вы хотите сделать? Введите команду: ',))

        match action:

            case '/add':
                print("Добавление книги")
            case '/all':
                print("Показать список всех книг")
            case '/delete':
                print("Удалить книгу")
            case '/search':
                print("Поиск книги")
            case '/change-status':
                print("Сменить статус книги")
            case _:
                print("Команда не распознана, повторите попытку")
                self.request_action()

