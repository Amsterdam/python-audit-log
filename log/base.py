import logging


class BaseLog:

    def __init__(self) -> None:
        super().__init__()
        self.level = logging.INFO
        self.message = ''

    def debug(self, msg):
        self.level = logging.DEBUG
        self.message = msg
        return self

    def info(self, msg):
        self.level = logging.INFO
        self.message = msg
        return self

    def warning(self, msg):
        self.level = logging.WARNING
        self.message = msg
        return self

    def error(self, msg):
        self.level = logging.ERROR
        self.message = msg
        return self

    def critical(self, msg):
        self.level = logging.CRITICAL
        self.message = msg
        return self
