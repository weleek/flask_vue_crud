# -*- coding: utf-8 -*-
import sys
import linecache
import traceback
import logging
import colorlog
from passlib.hash import pbkdf2_sha256


def print_stack_trace():
    exc_type, exc_obj, tb = sys.exc_info()
    stk = traceback.extract_tb(tb, 1)
    f = tb.tb_frame
    lineno = tb.tb_lineno
    funcname = stk[0][2]
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print(f'\x1b[1;37;41m[EXCEPTION]\x1b[0m {exc_type.__name__}: ', end='')
    print(f'Message "{exc_obj}", File "{filename}", Line {lineno}, in {funcname}\n\t{line.strip()}')


def logger_init(module_name='', level='INFO', logger=None):
    logger = logging.getLogger(module_name) if logger is None else logger
    logger.setLevel(level)
    fmt = '%(log_color)s%(levelname)6s %(asctime)s %(name)16s(%(lineno)4s) %(threadName)16s - %(message)s'
    formatter = colorlog.ColoredFormatter(fmt)
    handler = colorlog.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_request_data(request):
    if request.data == b'':
        return None
    return request.get_json()


def hash_password(password):
    return pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)


def verify_password(password, _hash):
    return pbkdf2_sha256.verify(password, _hash)
