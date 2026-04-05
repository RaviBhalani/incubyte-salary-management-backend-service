import sys

from .env_helpers import get_env_var


LOG_LEVEL = get_env_var("LOG_LEVEL")


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'stream': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
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
            'handlers': ['stream'],  # Handlers to be used for this logger
            'level': LOG_LEVEL,  # Minimum logging level
            'propagate': True,  # Whether to propagate messages to parent loggers
        },
    },
}
