from pathlib import Path
from config import PROJECT_BASE_DIR


BASE_DIR = Path(__file__).resolve().parent
JSON_ROOT_DIRECTORY = PROJECT_BASE_DIR / 'db/client/schedule/schedule.json'