import json
from logging import Formatter, LogRecord


class AuditLogFormatter(Formatter):

    def formatMessage(self, record: LogRecord) -> str:
        audit_str = json.dumps(record.audit) if hasattr(record, 'audit') else 'LogRecord misses audit attribute'
        return "audit: " + audit_str
