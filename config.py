# -*- coding: utf-8 -*-
import os
import sys
import yaml
import platform
from pathlib import Path


def is_windows():
    return platform.system().upper().find('WINDOWS') != -1


class Config:
    # 하위 모듈에서 각 패키지별 모듈을 참조 하기 위한 참조 경로 추가.
    WORK_DIR = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/'))
    DATABASE_HOME = f'{str(Path.home())}/mongodb/app'
    DATABASE_LOG_DIR = f'{DATABASE_HOME}/logs'
    LOGGING_DIR = f'{WORK_DIR}/logs'
    options = {}

    def __init__(self, argv=None):
        sys.path.append(f'{self.WORK_DIR}/app')

        if os.getcwd() != self.WORK_DIR:
            os.chdir(self.WORK_DIR)

        self.options = argv or {}
        with open(f"{self.WORK_DIR}/config.yaml", 'r') as stream:
            conf = yaml.safe_load(stream)
            self.options.update(conf)

        if self.options['logging']['level'].upper() == 'DEBUG':
            self.options['--debug'] = True
