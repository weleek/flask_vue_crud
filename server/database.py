# -*- coding: utf-8 -*-
import os
import signal
import datetime

import psutil
from flask_mongoengine import MongoEngine

from server.exceptions import ProcessException


def database_init(app, options):
    if not check_service():
        raise ProcessException('Database is not running...')

    app.config['MONGODB_SETTINGS'] = options['database']['settings']
    database = MongoEngine()
    database.init_app(app)


def check_service():
    #return ('mongod' in ( p.name() for p in psutil.process_iter()))
    return len(get_pids()) > 0


def get_pids():
    result = []
    for p in psutil.process_iter():
        if p.name() == 'mongod':
            result.append(p.pid)
    return result


def database_start(config):
    print('Database start...')
    if check_service():
        raise ProcessException('Database is already running...')

    if not os.path.exists(f'{config.DATABASE_HOME}'):
        os.makedirs(f'{config.DATABASE_HOME}')

    if not os.path.exists(f'{config.DATABASE_LOG_DIR}'):
        os.makedirs(f'{config.DATABASE_LOG_DIR}')

    if not os.access(f'{config.DATABASE_LOG_DIR}', os.W_OK):
        os.chmod(f'{config.DATABASE_LOG_DIR}', 0o777)

    os.system(f'mongod --fork --logpath {config.DATABASE_LOG_DIR}/database.log --logappend --dbpath {config.DATABASE_HOME}')


def database_shutdown():
    print('Database stop...')
    if not check_service():
        raise ProcessException('Database is not running...')
    #os.system(f'mongod --dbpath {DATABASE_HOME} --shutdown')

    for pid in get_pids():
        os.kill(pid, signal.SIGTERM)


def database_status():
    print('Database status...')
    if not check_service():
        raise ProcessException('Database is not running...')

    for pid in get_pids():
        p = psutil.Process(pid)
        print(f"{p.name()} {p.username()} {p.pid} {p.ppid()}", end=" ")
        print(f"{datetime.datetime.fromtimestamp(p.create_time()).strftime('%Y-%m-%d %H:%M:%S')}", end=" ")
        print(f"{' '.join(p.cmdline())}")


def main(config):
    try:
        if config.options['--status']:

            database_status()

        elif config.options['--start']:

            database_start(config)

        elif config.options['--stop']:

            database_shutdown()

        else:
            raise ProcessException("Check the options...")

    except Exception as err:
        raise err
