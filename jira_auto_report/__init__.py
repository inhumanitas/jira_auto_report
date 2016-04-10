# coding: utf-8

import logging.config
import logging


logger = logging.getLogger('')

ch = logging.StreamHandler()

formatter = logging.Formatter("%(levelname)s %(asctime)s %(message)s")
ch.setFormatter(formatter)

logger.addHandler(ch)
