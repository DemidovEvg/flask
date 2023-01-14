from pathlib import Path
from dotenv import load_dotenv
import os


BASE_DIR = Path(__file__).parent
load_dotenv()
dotenv_path = BASE_DIR.parent / '.env_extra'
load_dotenv(dotenv_path, override=True)

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

SECRET_KEY = os.getenv('SECRET_KEY')
WTF_CSRF_ENABLED = os.getenv('WTF_CSRF_ENABLED')
