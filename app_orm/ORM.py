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
        data: dict | None = None
        with path.open(mode='r', encoding='utf-8') as f:
            data = json.load(f)
        return data

    @staticmethod
    def dump_data(path: Path, data: dict):
        with path.open(mode='w', encoding='utf-8') as sf:
            json.dump(data, sf)


class BooksManager(ORM):

    def __init__(self):
        self._library_db: Path = DATA_BASE_LIBRARY_PATH
        self._service_db: Path = DATA_BASE_SERVICE_PATH
        self._library: dict = dict()

    def get_all_books(self) -> list:
        if not self._library:
            self._library = self.get_data(self._library_db)
        return self._library.get('books')
