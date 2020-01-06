#! -*- coding: utf-8 -*-
from config import Config


if __name__ == '__main__':
    # TEST MAIN
    config = Config()
    print(config.WORK_DIR)
    print(config.DATABASE_HOME)
    print(config.DATABASE_LOG_DIR)
