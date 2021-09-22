import datetime
import sys
import os
import logging
from logging.handlers import TimedRotatingFileHandler
import re

dirname = os.path.dirname(__file__)
dirname = os.path.join(dirname, '../logs')

if not os.path.exists(dirname):
    os.mkdir(dirname)

date = datetime.date.today().strftime('%Y%m%d')
FORMATTER = logging.Formatter("%(asctime)s — %(levelname)s — %(message)s")
LOG_FILE = os.path.join(dirname, 'my_app.' + date + '.log')


def getDate():
    global date
    return date

def namer(name):
    a = name[-28:][-8:]
    date1 = datetime.datetime.strptime(a, '%Y%m%d')
    date1 = date1 + datetime.timedelta(days=1)
    str_date = datetime.datetime.strftime(date1, '%Y%m%d')
    name = name.replace('.' + getDate() + '.log', '') + '.log'
    return name.replace(a, str_date)

def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight', backupCount=10, encoding='utf-8')
    file_handler.suffix = '%Y%m%d'
    file_handler.namer = namer
    file_handler.extMatch = re.compile(r"^\d{8}$")
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger


