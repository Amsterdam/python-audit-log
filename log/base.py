import logging


class BaseLog:

    level = logging.INFO
    message = ''

    def __init__(self):
        pass

    def debug(self, msg):
        self.level = logging.DEBUG
        self.message = msg

    def info(self, msg):
        self.level = logging.INFO
        self.message = msg

    def warning(self, msg):
        self.level = logging.WARNING
        self.message = msg

    def error(self, msg):
        self.level = logging.ERROR
        self.message = msg

    def critical(self, msg):
        self.level = logging.CRITICAL
        self.message = msg
