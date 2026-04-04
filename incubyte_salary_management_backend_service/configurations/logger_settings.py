from os.path import join
from .common_settings import BASE_DIR
from .env_helpers import get_env_var, get_int_env_var

LOG_MAX_FILE_SIZE = get_int_env_var("LOG_MAX_FILE_SIZE")
LOG_LEVEL = get_env_var("LOG_LEVEL")

LOG_FOLDER = "logs"
LOG_FILE = "request.log"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': join(BASE_DIR, LOG_FOLDER, LOG_FILE),
            'maxBytes': LOG_MAX_FILE_SIZE,  # Maximum file size in bytes before rotation
            'backupCount': 5,  # Number of backup files to keep
            'encoding': 'utf-8',  # Encoding for the log file
            'formatter': 'verbose',  # Log message format
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] %(message)s (%(filename)s:%(lineno)s)',  # Log message format
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],  # Handlers to be used for this logger
            'level': LOG_LEVEL,  # Minimum logging level
            'propagate': True,  # Whether to propagate messages to parent loggers
        },
    },
}