import json

from app_orm.ORM import ORM, BooksManager
from config import DATA_BASE_LIBRARY_PATH, DATA_BASE_SERVICE_PATH


class RunValidator:

    r"""Валидатор. Должен проверять состояние приложения перед запуском, создает необходимые файлы,
    в случае их отсутствия
    """

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
        orm = ORM()
        last_pk = None

        try:
            books_pk: list[int] = list(map(int, BooksManager().get_all_books().keys()))
            if books_pk:
                max_pk = max(books_pk)
                service_data = orm.get_service_data()
                if service_data:
                    last_pk = service_data.get('last_generated_pk', None)
                if last_pk is not None:
                    if last_pk != max_pk:
                        service_data['last_generated_pk'] = max_pk
                        orm.update_service_data(service_data)
                else:
                    new_service_data = cls.service_file_pattern.copy()
                    new_service_data['last_generated_pk'] = max_pk
                    orm.update_service_data(new_service_data)

        except json.decoder.JSONDecodeError:
            print("База данных библиотеки пуста. Решаю эту проблему")
            ORM.dump_data(DATA_BASE_LIBRARY_PATH, dict())
            ORM.dump_data(DATA_BASE_SERVICE_PATH, cls.service_file_pattern)

        except Exception as error:
            print("Произошла ошибка")
            raise error
