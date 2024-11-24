from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_BASE_LIBRARY_PATH: Path = BASE_DIR / 'db/library_db.json'

DATA_BASE_SERVICE_PATH: Path = BASE_DIR / 'db/service_data.json'

SUPPORTED_LANGUAGES = ['RU', 'EN']

LIBRARY_HEADERS = ['ID', 'Название', 'Автор', 'Год публикации', 'Статус']

DEFAULT_LOCALIZATION = 'RU'

INIT_MESSAGE = """\tДля большего удобства, введите, пожалуйста, язык, который удобен вам для работы.
\tFor greater convenience, please input the language you are comfortable with for your work
\tRU - Русский
\tEN - English
\t"""

WRONG_LANGUAGE = """\tВведен некорректный язык, повторите попытку
\tIncorrect language entered, try again"""
