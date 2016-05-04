# coding: utf-8

import logging

from jira_auto_report.settings import LOG_FILENAME, LOG_LEVEL
from jira_auto_report.logging_handlers import SMTPHandler

logger = logging.getLogger('')

# logger.setLevel(LOG_LEVEL)
logger.setLevel(10)

formatter = logging.Formatter("%(levelname)s %(asctime)s %(message)s")

ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

f = logging.FileHandler(LOG_FILENAME)
f.setFormatter(formatter)
logger.addHandler(f)


m = SMTPHandler(subject='jira auto report log',)
m.setFormatter(formatter)
m.setLevel(50)
logger.addHandler(m)
