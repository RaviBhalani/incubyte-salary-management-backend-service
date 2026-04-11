from pathlib import Path

from .env_helpers import get_env_var

BASE_DIR = Path(__file__).resolve().parent.parent.parent
APP_TITLE = 'API Service'
ENVIRONMENT = get_env_var("ENVIRONMENT")
