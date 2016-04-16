# coding: utf-8

import logging.config

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(levelname)s %(asctime)s %(message)s',
            'datefmt': '%m/%d/%Y %H:%M:%S',
        },
        'extended': {
            'format': '%(asctime)s - %(levelname)s - File: %(filename)s - '
                      '%(funcName)s() - Line: %(lineno)d - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        'jira_auto_report': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
        '__main__': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    }
}


logging.config.dictConfig(LOGGING)
