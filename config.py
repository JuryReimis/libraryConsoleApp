from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_BASE_LIBRARY_PATH: Path = BASE_DIR / 'db/library_db.json'

DATA_BASE_SERVICE_PATH: Path = BASE_DIR / 'db/service_data.json'
