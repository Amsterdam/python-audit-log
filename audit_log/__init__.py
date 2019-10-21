import logging
import sys

from audit_log.formatter import AuditLogFormatter

AUDIT_LOGGER_NAME = 'audit_log'

audit_logger = logging.getLogger(AUDIT_LOGGER_NAME)
audit_logger.setLevel(logging.INFO)
audit_logger.propagate = False

handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(AuditLogFormatter())
audit_logger.addHandler(handler)
