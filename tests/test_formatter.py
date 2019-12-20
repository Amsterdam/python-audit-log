from unittest import TestCase
from unittest.mock import patch, MagicMock

from audit_log.formatter import AuditLogFormatter


class TestFormatter(TestCase):

    @patch('logging.LogRecord')
    def test_format_message(self, mocked_record):
        audit = {'test': 'audit'}
        mocked_record.audit = audit
        formatter = AuditLogFormatter()
        message = formatter.formatMessage(mocked_record)
        expected_message = '{"audit": {"test": "audit"}}'
        self.assertEqual(message, expected_message)

    def test_format_message_missing_attr(self):
        # create a MagicMock object that will return false for all hasattr() calls.
        # this is needed to test what happens when the expected 'audit' attr
        # does not exist
        mocked_record = MagicMock(spec=[])
        formatter = AuditLogFormatter()
        message = formatter.formatMessage(mocked_record)
        expected_message = '{"audit": {"message": "LogRecord misses audit attribute"}}'
        self.assertEqual(message, expected_message)

