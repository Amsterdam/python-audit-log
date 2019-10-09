import logging

from logstash_async.handler import AsynchronousLogstashHandler

from audit_log import app_settings
from audit_log.formatter import AuditLogFormatter

audit_logger = logging.getLogger('audit_log')
audit_logger.setLevel(logging.INFO)

handler = AsynchronousLogstashHandler(
    transport='logstash_async.transport.TcpTransport',
    host=app_settings.AUDIT_LOG_LOGSTASH_HOST,
    port=app_settings.AUDIT_LOG_LOGSTASH_PORT,
    database_path='logstash.db')

handler.setFormatter(AuditLogFormatter())
audit_logger.addHandler(handler)
