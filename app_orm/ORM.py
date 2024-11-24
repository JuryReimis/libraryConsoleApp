import json
# import threading
from pathlib import Path

from config import DATA_BASE_LIBRARY_PATH, DATA_BASE_SERVICE_PATH


class ORM:
    r"""Базовый класс для взаимодействия с бд
    Представлены общие методы
    """

    @staticmethod
    def create_table(path: Path):
        r"""Создание файла по указанному пути.
        """
        with path.open(mode='w', encoding='utf-8'):
            pass

    @staticmethod
    def get_data(path: Path):
        r"""Получение данных из json файла
        """
        with path.open(mode='r', encoding='utf-8') as f:
            data = json.load(f)
        return data

    @staticmethod
    def dump_data(path: Path, data: dict):
        r"""Сохранение json данных в файл
        """
        with path.open(mode='w', encoding='utf-8') as sf:
            json.dump(data, sf, ensure_ascii=False, indent=4)

    def get_service_data(self):
        return self.get_data(DATA_BASE_SERVICE_PATH)

    def update_service_data(self, new_service_data: dict):
        self.dump_data(DATA_BASE_SERVICE_PATH, new_service_data)


# def _synchronized(func):
#     r"""Декоратор для применения блокировки к методу, пока он используется в одном из потоков
#     """
#     def wrapped(self, *args, **kwargs):
#         with self._lock:
#             return func(self, *args, **kwargs)
#     return wrapped


class BooksManager(ORM):
    r"""Класс для взаимодействия библиотеки с базой данных.
    Имеет атрибут класса _library, который доступен всем экземплярам класса и обновляется сразу у всех.
    Была идея реализации блоков для избежания "Эффекта гонки" при использовании приложения параллельно
    в нескольких потоках. Пока излишне, хотя каркас оставил закомментированным.
    """
    _library: dict = dict()
    # _lock: threading.Lock = threading.Lock()

    def __init__(self):
        self._library_db: Path = DATA_BASE_LIBRARY_PATH
        self._service_db: Path = DATA_BASE_SERVICE_PATH
        self.localization = None

    def set_localization(self, localization=None):

        if localization is None:
            from localizations.loc_RU import LocalizationConstants
            self.localization = LocalizationConstants
        else:
            self.localization = localization

    # @_synchronized
    def get_all_books(self) -> dict:
        r"""Получение словаря со всеми книгами библиотеки
        В формате
        "id": {
            "id": id,
            "title": title,
            "author": author,
            "year": year,
            "status": status,
        }
        """
        if not self._library:
            self._library = self.get_data(self._library_db)
        return self._library.get('books')

    # @_synchronized
    def add_new_book(self, title: str, author: str, year: str):
        r"""Добавляет новую книгу в базу данных.
        """
        last_pk = self.get_service_data().get('last_generated_pk')
        new_book = {
            'id': last_pk + 1,
            'title': title,
            'author': author,
            'year': year,
            'status': 'в наличии'
        }
        books = self.get_all_books()
        books[str(last_pk + 1)] = new_book
        self._library['books'] = books
        try:
            self.update_library_db()
        except Exception as error:
            print(self.localization.ADD_BOOK_ERROR, error)
        else:
            self.update_last_pk()

    # @_synchronized
    def delete_books(self, ids: list[str]) -> (list, list):
        r"""Удаляет книги по списку id
        """
        try:
            deleted_books = []
            not_exist_books = []
            books = self.get_all_books()
            for i in ids:
                deleted_book: dict | None = books.pop(i, None)
                if deleted_book:
                    deleted_books.append(deleted_book)
                else:
                    not_exist_books.append(f'''{self.localization.TRY_DELETE_NOT_EXIST_ID_ERROR} {i}''')
            self._library['books'] = books
            self.update_library_db()
            return deleted_books, not_exist_books
        except Exception as error:
            return f'{self.localization.JUST_ERROR}\n{error}'

    def update_status(self, pk: str, new_status: str) -> str | None:
        r"""Обновляет статус книги в базе данных
        """
        try:
            books = self.get_all_books()
            book = books.get(pk)
            book['status'] = new_status
            self._library['books'] = books
            self.update_library_db()
        except Exception as error:
            return f"{self.localization.JUST_ERROR}\n{error}"
        else:
            return None

    def update_library_db(self):
        r"""Сохраняет обновленную библиотеку в бд
        """
        self.dump_data(self._library_db, self._library)

    def update_last_pk(self):
        r"""Обновляет последний используемый в бд индекс книги
        """
        service_data = self.get_service_data()
        service_data['last_generated_pk'] += 1
        self.update_service_data(service_data)
