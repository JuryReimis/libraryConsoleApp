import json

from app_orm.ORM import ORM, BooksManager
from config import DATA_BASE_LIBRARY_PATH, DATA_BASE_SERVICE_PATH


class RunValidator:

    r"""Валидатор. Должен проверять состояние приложения перед запуском, создает необходимые файлы,
    в случае их отсутствия"""

    service_file_pattern: dict = {
        'last_generated_pk': 0
    }

    @classmethod
    def check_db(cls):
        base_file = DATA_BASE_LIBRARY_PATH
        service_file = DATA_BASE_SERVICE_PATH
        if not base_file.exists():
            try:
                ORM.create_table(base_file)
            except Exception as error:
                print("Произошла ошибка при создании базы данных библиотекаря, обратитесь в технический отдел")
                raise error

        if not service_file.exists():
            try:
                ORM.dump_data(service_file, cls.service_file_pattern)
            except Exception as error:
                print("Произошла ошибка при создании служебной базы данных, обратитесь в технический отдел")
                raise error

    @classmethod
    def check_last_generated_pk(cls):
        service_file = DATA_BASE_SERVICE_PATH
        last_pk = None

        try:
            books: list = BooksManager().get_all_books()
            if books:
                max_pk = max([book.get('id') for book in books])
                service_data = ORM.get_data(service_file)
                if service_data:
                    last_pk = service_data.get('last_generated_pk')
                if last_pk:
                    if last_pk != max_pk:
                        service_data['last_generated_pk'] = max_pk
                        ORM.dump_data(service_file, service_data)
                else:
                    ORM.dump_data(service_file, cls.service_file_pattern)

        except json.decoder.JSONDecodeError:
            print("База данных библиотеки пуста. Решаю эту проблему")
            ORM.dump_data(DATA_BASE_LIBRARY_PATH, dict())
            ORM.dump_data(DATA_BASE_SERVICE_PATH, cls.service_file_pattern)

        except Exception as error:
            print("Произошла ошибка")
            raise error
