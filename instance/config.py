from pathlib import Path

BASE_DIR = Path(__file__).parent


DATABASE = f'sqlite:///{BASE_DIR}/demidov.sqlite'
