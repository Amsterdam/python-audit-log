from unittest import TestCase
from unittest.mock import patch

from audit_log.formatter import AuditLogFormatter


class TestFormatter(TestCase):

    @patch('logging.LogRecord')
    def test_format_message(self, mocked_record):
        audit = {'test': 'audit'}
        mocked_record.audit = audit
        formatter = AuditLogFormatter()
        message = formatter.formatMessage(mocked_record)
        expected_message = 'audit: {"test": "audit"}'
        self.assertEqual(message, expected_message)
