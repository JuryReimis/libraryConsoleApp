import json

from app_orm.ORM import ORM
from config import DATA_BASE_FILE_PATH, DATA_BASE_SERVICE_DATA_PATH


class RunValidator:

    r"""Валидатор. Должен проверять состояние приложения перед запуском, создает необходимые файлы,
    в случае их отсутствия"""

    service_file_pattern: dict = {
        'last_generated_pk': 0
    }

    @classmethod
    def check_db(cls):
        base_file = DATA_BASE_FILE_PATH
        service_file = DATA_BASE_SERVICE_DATA_PATH
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
