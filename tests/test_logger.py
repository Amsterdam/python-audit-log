import logging
import sys
from unittest import TestCase
from unittest.mock import patch, Mock

from audit_log.formatter import AuditLogFormatter
from audit_log.logger import AuditLogger


class TestAuditlogger(TestCase):

    def setUp(self) -> None:
        self.audit_log = AuditLogger()

    def test_default_logger_name(self):
        self.assertEqual(self.audit_log.get_logger_name(), 'audit_log')

    def test_default_log_handler(self):
        handler = self.audit_log.get_log_handler()
        self.assertIsInstance(handler, logging.StreamHandler)
        self.assertEqual(handler.stream, sys.stdout)

    def test_default_log_formatter(self):
        formatter = self.audit_log.get_log_formatter()
        self.assertIsInstance(formatter, AuditLogFormatter)

    @patch('audit_log.logger.AuditLogger.get_log_formatter')
    @patch('audit_log.logger.AuditLogger.get_log_handler')
    @patch('audit_log.logger.AuditLogger.get_logger_name')
    def test_init_logger(self, mocked_get_logger_name, mocked_get_log_handler, mocked_get_log_formatter):
        mocked_name = 'audit_logger_name'
        mocked_handler = Mock()
        mocked_formatter = Mock()
        mocked_get_logger_name.return_value = mocked_name
        mocked_get_log_handler.return_value = mocked_handler
        mocked_get_log_formatter.return_value = mocked_formatter

        # because we are mocking parts of the AuditLogger, we can not
        # use the self.audit_logger created in setUp(), but we need to
        # recreate it here!
        logger = AuditLogger().init_logger()
        self.assertEqual(logger.name, mocked_name)
        self.assertEqual(logger.level, logging.INFO)
        self.assertFalse(logger.propagate)

        handlers = logger.handlers
        self.assertEqual(len(handlers), 1)
        handler = handlers[0]
        self.assertEqual(handler, mocked_handler)
        mocked_handler.setFormatter.assert_called_with(mocked_formatter)

    @patch('audit_log.logger.AuditLogger.get_logger_name')
    def test_multiple_init_logger(self, mocked_get_logger_name):
        # we ran into an issue where each instance of AuditLogger would add an extra log handler
        # here we test and assert that multiple calls to init_logger() will not add more handlers
        # to the main logger object.
        mocked_name = 'audit_logger_name'
        mocked_get_logger_name.return_value = mocked_name

        # ensure no handlers exist
        logger = logging.getLogger(mocked_name)
        for handler in logger.handlers:
            logger.removeHandler(handler)

        self.assertEqual(len(logger.handlers), 0, "Expected 0 handlers, but found: {}".format(logger.handlers))
        AuditLogger().init_logger()
        self.assertEqual(len(logger.handlers), 1, "Expected 1 handler, but found: {}".format(logger.handlers))
        AuditLogger().init_logger()
        self.assertEqual(len(logger.handlers), 1, "Expected 1 handler, but found: {}".format(logger.handlers))

    def test_default_log_level(self):
        self.assertEqual(self.audit_log.level, logging.INFO)
        self.assertEqual(self.audit_log.message, '')
        self.assertIsNone(self.audit_log.http_request)
        self.assertIsNone(self.audit_log.http_response)
        self.assertIsNone(self.audit_log.user)
        self.assertIsNone(self.audit_log.filter)
        self.assertIsNone(self.audit_log.results)

    def test_debug(self):
        self.audit_log.debug('test')
        self.assertEqual(self.audit_log.level, logging.DEBUG)
        self.assertEqual(self.audit_log.message, 'test')

    def test_info(self):
        self.audit_log.info('test')
        self.assertEqual(self.audit_log.level, logging.INFO)
        self.assertEqual(self.audit_log.message, 'test')

    def test_warning(self):
        self.audit_log.warning('test')
        self.assertEqual(self.audit_log.level, logging.WARNING)
        self.assertEqual(self.audit_log.message, 'test')

    def test_error(self):
        self.audit_log.error('test')
        self.assertEqual(self.audit_log.level, logging.ERROR)
        self.assertEqual(self.audit_log.message, 'test')

    def test_critical(self):
        self.audit_log.critical('test')
        self.assertEqual(self.audit_log.level, logging.CRITICAL)
        self.assertEqual(self.audit_log.message, 'test')

    def test_set_http_request(self):
        self.audit_log.set_http_request(method='GET', url='http://localhost/', user_agent='test_agent')

        self.assertEqual(self.audit_log.http_request['method'], 'GET')
        self.assertEqual(self.audit_log.http_request['url'], 'http://localhost/')
        self.assertEqual(self.audit_log.http_request['user_agent'], 'test_agent')

    def test_set_http_response(self):
        self.audit_log.set_http_response(status_code=200, reason='OK', headers={'Test': 'test'})

        self.assertEqual(self.audit_log.http_response['status_code'], 200)
        self.assertEqual(self.audit_log.http_response['reason'], 'OK')
        self.assertEqual(self.audit_log.http_response['headers']['Test'], 'test')

    def test_set_user(self):
        self.audit_log.set_user(
            authenticated=True, provider='test', email='username@host.com',
            roles=['role1', 'role2'], ip='12.23.34.45', realm='testrealm',
            username='username'
        )

        self.assertEqual(self.audit_log.user['authenticated'], True)
        self.assertEqual(self.audit_log.user['provider']['name'], 'test')
        self.assertEqual(self.audit_log.user['provider']['realm'], 'testrealm')
        self.assertEqual(self.audit_log.user['email'], 'username@host.com')
        self.assertEqual(self.audit_log.user['roles'], ['role1', 'role2'])
        self.assertEqual(self.audit_log.user['ip'], '12.23.34.45')
        self.assertEqual(self.audit_log.user['username'], 'username')

    def test_set_filter(self):
        self.audit_log.set_filter(object_name='objname', kwargs={'field': 'filter'})
        self.assertEqual(self.audit_log.filter['object'], 'objname')
        self.assertEqual(self.audit_log.filter['kwargs'], {'field': 'filter'})

    def test_set_results(self):
        test_results = [
            'There are the results',
            ['this', 'is', 'a', 'list'],
            {'this': 'is', 'a': 'dict'},
            123
        ]
        for results in test_results:
            self.audit_log.set_results(results)
            self.assertEqual(self.audit_log.results, results)

    def test_extras_http_request(self):
        self.audit_log.set_http_request(method='GET', url='http://localhost/', user_agent='test_agent')

        extras = self.audit_log._get_extras(log_type='test')
        self.assertIn('http_request', extras)
        self.assertEqual(extras['http_request']['method'], 'GET')
        self.assertEqual(extras['http_request']['url'], 'http://localhost/')
        self.assertEqual(extras['http_request']['user_agent'], 'test_agent')

    def test_extras_http_response(self):
        self.audit_log.set_http_response(status_code=200, reason='OK', headers={'Test': 'test'})

        extras = self.audit_log._get_extras(log_type='test')
        self.assertIn('http_response', extras)
        self.assertEqual(extras['http_response']['status_code'], 200)
        self.assertEqual(extras['http_response']['reason'], 'OK')
        self.assertEqual(extras['http_response']['headers']['Test'], 'test')

    def test_extras_user(self):
        self.audit_log.set_user(
            authenticated=True, provider='test', email='username@host.com',
            roles=['role1', 'role2'], ip='12.23.34.45', realm='testrealm',
            username='username'
        )

        extras = self.audit_log._get_extras(log_type='test')
        self.assertIn('user', extras)
        self.assertEqual(extras['user']['authenticated'], True)
        self.assertEqual(extras['user']['provider']['name'], 'test')
        self.assertEqual(extras['user']['provider']['realm'], 'testrealm')
        self.assertEqual(extras['user']['email'], 'username@host.com')
        self.assertEqual(extras['user']['roles'], ['role1', 'role2'])
        self.assertEqual(extras['user']['ip'], '12.23.34.45')
        self.assertEqual(extras['user']['username'], 'username')

    def test_extras_filter(self):
        self.audit_log.set_filter(object_name='objname', kwargs={'field': 'filter'})

        extras = self.audit_log._get_extras(log_type='test')
        self.assertIn('filter', extras)
        self.assertEqual(extras['filter']['object'], 'objname')
        self.assertEqual(extras['filter']['kwargs'], {'field': 'filter'})

    def test_extras_results(self):
        test_results = [
            'There are the results',
            ['this', 'is', 'a', 'list'],
            {'this': 'is', 'a': 'dict'},
            123
        ]
        for results in test_results:
            self.audit_log.set_results(results)
            extras = self.audit_log._get_extras(log_type='test')
            self.assertIn('results', extras)
            self.assertEqual(extras['results'], results)

    def test_extras_logtype(self):
        extras = self.audit_log._get_extras(log_type='test_type')
        self.assertEqual(extras['type'], 'test_type')

    @patch('audit_log.logger.AuditLogger.init_logger')
    def test_send_log_info(self, mocked_init_logger):
        mocked_logger = Mock()
        mocked_init_logger.return_value = mocked_logger

        # because we are mocking parts of the AuditLogger, we can not
        # use the self.audit_logger created in setUp(), but we need to
        # recreate it here!
        audit_log = AuditLogger()
        extected_extra = {'audit': {
                'http_request': None,
                'http_response': None,
                'user': None,
                'filter': None,
                'results': None,
                'type': 'INFO',
                'message': 'message'
            }
        }

        audit_log.info("message").send_log()
        mocked_logger.log.assert_called_with(
            level=logging.INFO,
            msg='message',
            extra=extected_extra
        )

