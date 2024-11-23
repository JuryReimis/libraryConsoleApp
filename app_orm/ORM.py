import json
# import threading
from pathlib import Path

from config import DATA_BASE_LIBRARY_PATH, DATA_BASE_SERVICE_PATH


class ORM:

    @staticmethod
    def create_table(path: Path):
        with path.open(mode='w', encoding='utf-8'):
            pass

    @staticmethod
    def get_data(path: Path):
        with path.open(mode='r', encoding='utf-8') as f:
            data = json.load(f)
        return data

    @staticmethod
    def dump_data(path: Path, data: dict):
        with path.open(mode='w', encoding='utf-8') as sf:
            json.dump(data, sf, ensure_ascii=False, indent=4)

    def get_service_data(self):
        return self.get_data(DATA_BASE_SERVICE_PATH)

    def update_service_data(self, new_service_data: dict):
        self.dump_data(DATA_BASE_SERVICE_PATH, new_service_data)


# def _synchronized(func):
#     def wrapped(self, *args, **kwargs):
#         with self._lock:
#             return func(self, *args, **kwargs)
#     return wrapped


class BooksManager(ORM):
    _library: dict = dict()
    # _lock: threading.Lock = threading.Lock()

    def __init__(self):
        self._library_db: Path = DATA_BASE_LIBRARY_PATH
        self._service_db: Path = DATA_BASE_SERVICE_PATH

    # @_synchronized
    def get_all_books(self) -> dict:
        if not self._library:
            self._library = self.get_data(self._library_db)
        return self._library.get('books')

    # @_synchronized
    def add_new_book(self, title: str, author: str, year: str):
        last_pk = self.get_service_data().get('last_generated_pk')
        new_book = {
            'id': last_pk + 1,
            'title': title,
            'author': author,
            'year': year,
            'status': 'В наличии'
        }
        books = self.get_all_books()
        books[str(last_pk + 1)] = new_book
        self._library['books'] = books
        try:
            self.update_library_db()
        except Exception as error:
            print("Произошла ошибка при добавлении книги, обратитесь в технический отдел.", error)
        else:
            self.update_last_pk()

    # @_synchronized
    def delete_books(self, ids: list[str]) -> bool:
        try:
            books = self.get_all_books()
            for i in ids:
                deleted_book: dict | None = books.pop(i, None)
                if deleted_book:
                    print(f'''Удалена книга 
                    id: {deleted_book.get('id')} 
                    Название: {deleted_book.get('title')}
                    Автор: {deleted_book.get('author')}
                    Год издания: {deleted_book.get('year')}''')
                else:
                    print(f'''Попытка удалить несуществующую книгу с id {i}''')
            self._library['books'] = books
            self.update_library_db()
            return True
        except Exception as error:
            print('Произошла ошибка', error, sep='\n')
            return False

    def update_status(self, pk: str, new_status: str) -> str | None:
        try:
            books = self.get_all_books()
            book = books.get(pk)
            book['status'] = new_status
            self._library['books'] = books
            self.update_library_db()
        except Exception as error:
            return f"Произошла ошибка, просьба обратиться в технический отдел\n{error}"
        else:
            return None

    def update_library_db(self):
        self.dump_data(self._library_db, self._library)

    def update_last_pk(self):
        service_data = self.get_service_data()
        service_data['last_generated_pk'] += 1
        self.update_service_data(service_data)
