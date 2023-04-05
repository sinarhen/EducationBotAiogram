import os
from dotenv import find_dotenv, load_dotenv
from pathlib import Path

load_dotenv(find_dotenv())

PROJECT_BASE_DIR = Path(__file__).resolve().parent
API_TOKEN = os.getenv("API_TOKEN")


PLOTS_DIRECTORY = PROJECT_BASE_DIR / 'plots/'
