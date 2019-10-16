import logging
import sys

from audit_log import app_settings
from audit_log.formatter import AuditLogFormatter

audit_logger = logging.getLogger(app_settings.AUDIT_LOG_LOGGER_NAME)
audit_logger.setLevel(logging.INFO)
audit_logger.propagate = False

handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(AuditLogFormatter())
audit_logger.addHandler(handler)
