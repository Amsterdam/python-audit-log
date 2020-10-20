import json
from logging import Formatter, LogRecord


class AuditLogFormatter(Formatter):

    def formatMessage(self, record: LogRecord) -> str:
        if hasattr(record, 'audit'):
            audit = {'audit': record.audit}
        else:
            audit = {'audit': {'message': 'LogRecord misses audit attribute'}}

        return json.dumps(audit)
