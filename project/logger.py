import logging
from logging.config import dictConfig
from pathlib import Path


logger_config = dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': Path(__file__).parent.parent/'log'/'common.log',
            'formatter': 'default'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
    },
    'loggers': {
        'root': {
            'level': 'INFO',
            'handlers': ['file', 'console']
        },
        'sqlalchemy.engine': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False
        }
    }
})
logging.getLogger('werkzeug').handlers = []
