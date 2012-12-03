# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

import logging

logger = logging.getLogger('matarisvan')
logger.setLevel(logging.DEBUG)

logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)

logger.addHandler(ch)


