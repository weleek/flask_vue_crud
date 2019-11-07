# -*- coding: utf-8 -*-
# default libs
import os
import datetime
import importlib
import signal

# 3rd party libs
import psutil
from flask import Flask
from gevent.pywsgi import WSGIServer

# custom develop libs
from server.exceptions import ProcessException
from server.database import database_init
from server.common.utils import logger_init


def web_init(app, options):
    if options['--debug']:
        app.jinja_env.auto_reload = options['--debug']
        app.debug = options['--debug']
        app.env = 'development'

    for controller in os.listdir(f'{os.path.dirname(os.path.realpath(__file__))}/controllers'):
        if controller[:2] == '__':
            continue

        controller = importlib.import_module(f"{__package__}.controllers.{controller.replace('.py', '')}")
        app.register_blueprint(controller.app, url_prefix=controller.url_prefix)


def create_app(options):
    app = Flask(__name__)
    web_init(app, options)
    try:
        database_init(app, options)
    except Exception as e:
        print(f'{e}')
    return app


def get_pids():
    result = []
    for p in psutil.process_iter():
        try:
            cmdlines = ' '.join(p.cmdline())
            if cmdlines.find('flask_app') != -1 and cmdlines.find('gunicorn') != -1:
                result.append(p.pid)
        except:
            continue
    return result


def check_service():
    return len(get_pids()) > 0


def web_start(config):
    print("Web service start...")
    if check_service():
        raise ProcessException('Web service is already running...')

    if not os.path.exists(f'{config.LOGGING_DIR}'):
        os.makedirs(f'{config.LOGGING_DIR}')

    if not os.access(f'{config.LOGGING_DIR}', os.W_OK):
        os.chmod(f'{config.LOGGING_DIR}', 0o777)

    cmd = ' '.join(['gunicorn',
                    '--name=flask_app',
                    f'--chdir={config.WORK_DIR}',
                    f'\'{__name__}:create_app({{"--debug": {config.options["--debug"]} }})\'',
                    f'--bind=0.0.0.0:{config.options["server"]["port"]}',
                    '--daemon',
                    '--workers=2',
                    f'--log-level={config.options["logging"]["level"]}',
                    f'--access-logfile="{config.LOGGING_DIR}/web_access.log"',
                    f'--error-logfile="{config.LOGGING_DIR}/web_error.log"',
                    '--reload' if config.options["--debug"] else ''])
    print(cmd)
    os.system(cmd)


def web_shutdown():
    print("Web service shutdown...")
    if not check_service():
        raise ProcessException('Web service is not running...')

    for pid in get_pids():
        os.kill(pid, signal.SIGTERM)


def web_status():
    print("Web service status...")
    if not check_service():
        raise ProcessException('Web service is not running...')

    for pid in get_pids():
        p = psutil.Process(pid)
        print(f"{p.name()} {p.username()} {p.pid} {p.ppid()}", end=" ")
        print(f"{datetime.datetime.fromtimestamp(p.create_time()).strftime('%Y-%m-%d %H:%M:%S')}", end=" ")
        print(f"{' '.join(p.cmdline())}")


def main(config):
    try:
        if config.options['--status']:

            web_status()

        elif config.options['--start']:

            web_start(config)

        elif config.options['--stop']:

            web_shutdown()

        else:
            raise ProcessException("Check the options...")

    except Exception as err:
        raise err
