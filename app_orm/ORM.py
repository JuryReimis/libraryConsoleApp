import json
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


class BooksManager(ORM):

    def __init__(self):
        self._library_db: Path = DATA_BASE_LIBRARY_PATH
        self._service_db: Path = DATA_BASE_SERVICE_PATH
        self._library: dict = dict()

    def get_all_books(self) -> dict:
        if not self._library:
            self._library = self.get_data(self._library_db)
        return self._library.get('books')

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
            self.dump_data(DATA_BASE_LIBRARY_PATH, self._library)
        except Exception as error:
            print("Произошла ошибка при добавлении книги, обратитесь в технический отдел.", error)
        else:
            self.update_last_pk()

    def delete_books(self, ids: list[int]) -> bool:
        pass

    def update_last_pk(self):
        service_data = self.get_service_data()
        service_data['last_generated_pk'] += 1
        self.update_service_data(service_data)
