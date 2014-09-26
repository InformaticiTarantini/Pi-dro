__author__ = 'walter'

import logging

from flask import Flask
from settings import Settings

app = Flask(__name__, static_url_path='/static')
app.config.from_object(Settings())

log = logging.getLogger(app.config.get("LOGGER_NAME"))
log.setLevel(app.config.get("LOGGER_LEVEL"))
ch = logging.StreamHandler()
ch.setLevel(app.config.get("LOGGER_LEVEL"))
formatter = logging.Formatter('[%(asctime)s] %(name)s <%(levelname)s> %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)

