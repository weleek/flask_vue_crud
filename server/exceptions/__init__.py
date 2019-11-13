from . import *


class ProcessException(Exception):
    pass


class QuitException(Exception):
    pass


class ArgsException(Exception):
    pass


class ValidationError(Exception):
    pass


class UnavailableContentError(Exception):
    pass


class DatabaseProcessError(Exception):
    pass
