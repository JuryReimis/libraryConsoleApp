from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_BASE_LIBRARY_PATH: Path = BASE_DIR / 'db/library_db.json'

DATA_BASE_SERVICE_PATH: Path = BASE_DIR / 'db/service_data.json'

LIBRARY_HEADERS = ['ID', 'Название', 'Автор', 'Год публикации', 'Статус']

HELLO_MESSAGE: str = """\tПриветствую вас в приложении для обслуживания библиотеки. Здесь есть несколько функций.
\tВы можете добавлять книги, удалять их, менять их статус. Вы можете посмотреть полный список всех книг и
\tнайти все книги по названию, автору и году издания. Приступайте к работе:"""

FUNCTIONAL_DESCRIPTION: str = """\tПросмотреть список всех книг: /all
\tДобавить книгу: /add
\tУдалить книгу: /delete
\tПоиск книги: /search
\tИзменить статус книги: /change-status
\tВыйти из приложения: /exit"""
