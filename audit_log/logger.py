import logging
import sys

from audit_log.formatter import AuditLogFormatter

AUDIT_LOGGER_NAME = 'audit_log'


class AuditLogger:

    def __init__(self) -> None:
        super().__init__()

        self.logger = self.init_logger()

        self.level = logging.INFO
        self.message = ''
        self.http_request = None
        self.http_response = None
        self.user = None
        self.filter = None
        self.results = None

    def init_logger(self) -> logging.Logger:
        logger = logging.getLogger(self.get_logger_name())
        logger.setLevel(logging.INFO)
        logger.propagate = False

        if not logger.hasHandlers():
            handler = self.get_log_handler()
            formatter = self.get_log_formatter()
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def get_logger_name(self) -> str:
        return AUDIT_LOGGER_NAME

    def get_log_handler(self) -> logging.Handler:
        return logging.StreamHandler(stream=sys.stdout)

    def get_log_formatter(self) -> logging.Formatter:
        return AuditLogFormatter()

    def debug(self, msg: str) -> 'AuditLogger':
        self.level = logging.DEBUG
        self.message = msg
        return self

    def info(self, msg: str) -> 'AuditLogger':
        self.level = logging.INFO
        self.message = msg
        return self

    def warning(self, msg: str) -> 'AuditLogger':
        self.level = logging.WARNING
        self.message = msg
        return self

    def error(self, msg: str) -> 'AuditLogger':
        self.level = logging.ERROR
        self.message = msg
        return self

    def critical(self, msg: str) -> 'AuditLogger':
        self.level = logging.CRITICAL
        self.message = msg
        return self

    def set_http_request(self, method: str, url: str, user_agent: str = '') -> 'AuditLogger':
        self.http_request = {
            'method': method,
            'url': url,
            'user_agent': user_agent
        }
        return self

    def set_http_response(self, status_code: int, reason: str, headers: dict = None) -> 'AuditLogger':
        self.http_response = {
            'status_code': status_code,
            'reason': reason,
            'headers': headers
        }
        return self

    def set_user(self, authenticated: bool, provider: str, email: str,
                 roles: list = None, ip: str = '', realm: str = '') -> 'AuditLogger':
        self.user = {
            'authenticated': authenticated,
            'email': email,
            'roles': roles,
            'ip': ip,
            'provider': {
                'name': provider,
                'realm': realm,
            }
        }
        return self

    def set_filter(self, object_name: str, kwargs: dict) -> 'AuditLogger':
        self.filter = {
            'object': object_name,
            'kwargs': kwargs,
        }
        return self

    def set_results(self, results: list) -> 'AuditLogger':
        self.results = results
        return self

    def send_log(self) -> None:
        self.logger.log(
            level=self.level,
            msg=self.message,
            extra={'audit': self._get_extras(logging.getLevelName(self.level))})

    def _get_extras(self, log_type: str) -> dict:
        return {
            'http_request': self.http_request,
            'http_response': self.http_response,
            'user': self.user,
            'filter': self.filter,
            'results': self.results,
            'type': log_type,
            'message': self.message
        }
