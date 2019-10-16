import json
from logging import Formatter


class AuditLogFormatter(Formatter):

    def formatMessage(self, record):
        return "audit: " + json.dumps(record.audit)
