import logging
from unittest import TestCase
from unittest.mock import patch

from audit_log.logger import AuditLogger


class TestAuditlogger(TestCase):

    def test_default_log_level(self):
        audit_log = AuditLogger()
        self.assertEqual(audit_log.level, logging.INFO)
        self.assertEqual(audit_log.message, '')
        self.assertIsNone(audit_log.http_request)
        self.assertIsNone(audit_log.http_response)
        self.assertIsNone(audit_log.user)
        self.assertIsNone(audit_log.filter)
        self.assertIsNone(audit_log.results)

    def test_debug(self):
        audit_log = AuditLogger()
        audit_log.debug('test')
        self.assertEqual(audit_log.level, logging.DEBUG)
        self.assertEqual(audit_log.message, 'test')

    def test_info(self):
        audit_log = AuditLogger()
        audit_log.info('test')
        self.assertEqual(audit_log.level, logging.INFO)
        self.assertEqual(audit_log.message, 'test')

    def test_warning(self):
        audit_log = AuditLogger()
        audit_log.warning('test')
        self.assertEqual(audit_log.level, logging.WARNING)
        self.assertEqual(audit_log.message, 'test')

    def test_error(self):
        audit_log = AuditLogger()
        audit_log.error('test')
        self.assertEqual(audit_log.level, logging.ERROR)
        self.assertEqual(audit_log.message, 'test')

    def test_critical(self):
        audit_log = AuditLogger()
        audit_log.critical('test')
        self.assertEqual(audit_log.level, logging.CRITICAL)
        self.assertEqual(audit_log.message, 'test')

    def test_set_http_request(self):
        audit_log = AuditLogger()
        audit_log.set_http_request(method='GET', url='http://localhost/', user_agent='test_agent')

        self.assertEqual(audit_log.http_request['method'], 'GET')
        self.assertEqual(audit_log.http_request['url'], 'http://localhost/')
        self.assertEqual(audit_log.http_request['user_agent'], 'test_agent')

    def test_set_http_response(self):
        audit_log = AuditLogger()
        audit_log.set_http_response(status_code=200, reason='OK', headers={'Test': 'test'})

        self.assertEqual(audit_log.http_response['status_code'], 200)
        self.assertEqual(audit_log.http_response['reason'], 'OK')
        self.assertEqual(audit_log.http_response['headers']['Test'], 'test')

    def test_set_user(self):
        audit_log = AuditLogger()
        audit_log.set_user(
            authenticated=True, provider='test', email='username@host.com',
            roles=['role1', 'role2'], ip='12.23.34.45', realm='testrealm'
        )

        self.assertEqual(audit_log.user['authenticated'], True)
        self.assertEqual(audit_log.user['provider']['name'], 'test')
        self.assertEqual(audit_log.user['provider']['realm'], 'testrealm')
        self.assertEqual(audit_log.user['email'], 'username@host.com')
        self.assertEqual(audit_log.user['roles'], ['role1', 'role2'])
        self.assertEqual(audit_log.user['ip'], '12.23.34.45')

    def test_set_filter(self):
        audit_log = AuditLogger()
        audit_log.set_filter(object_name='objname', kwargs={'field': 'filter'})
        self.assertEqual(audit_log.filter['object'], 'objname')
        self.assertEqual(audit_log.filter['kwargs'], {'field': 'filter'})

    def test_set_results(self):
        audit_log = AuditLogger()
        test_results = [
            'There are the results',
            ['this', 'is', 'a', 'list'],
            {'this': 'is', 'a': 'dict'},
            123
        ]
        for results in test_results:
            audit_log.set_results(results)
            self.assertEqual(audit_log.results, results)

    def test_extras_http_request(self):
        audit_log = AuditLogger()
        audit_log.set_http_request(method='GET', url='http://localhost/', user_agent='test_agent')

        extras = audit_log._get_extras(log_type='test')
        self.assertIn('http_request', extras)
        self.assertEqual(extras['http_request']['method'], 'GET')
        self.assertEqual(extras['http_request']['url'], 'http://localhost/')
        self.assertEqual(extras['http_request']['user_agent'], 'test_agent')

    def test_extras_http_response(self):
        audit_log = AuditLogger()
        audit_log.set_http_response(status_code=200, reason='OK', headers={'Test': 'test'})

        extras = audit_log._get_extras(log_type='test')
        self.assertIn('http_response', extras)
        self.assertEqual(extras['http_response']['status_code'], 200)
        self.assertEqual(extras['http_response']['reason'], 'OK')
        self.assertEqual(extras['http_response']['headers']['Test'], 'test')

    def test_extras_user(self):
        audit_log = AuditLogger()
        audit_log.set_user(
            authenticated=True, provider='test', email='username@host.com',
            roles=['role1', 'role2'], ip='12.23.34.45', realm='testrealm'
        )

        extras = audit_log._get_extras(log_type='test')
        self.assertIn('user', extras)
        self.assertEqual(extras['user']['authenticated'], True)
        self.assertEqual(extras['user']['provider']['name'], 'test')
        self.assertEqual(extras['user']['provider']['realm'], 'testrealm')
        self.assertEqual(extras['user']['email'], 'username@host.com')
        self.assertEqual(extras['user']['roles'], ['role1', 'role2'])
        self.assertEqual(extras['user']['ip'], '12.23.34.45')

    def test_extras_filter(self):
        audit_log = AuditLogger()
        audit_log.set_filter(object_name='objname', kwargs={'field': 'filter'})

        extras = audit_log._get_extras(log_type='test')
        self.assertIn('filter', extras)
        self.assertEqual(extras['filter']['object'], 'objname')
        self.assertEqual(extras['filter']['kwargs'], {'field': 'filter'})

    def test_extras_results(self):
        audit_log = AuditLogger()
        test_results = [
            'There are the results',
            ['this', 'is', 'a', 'list'],
            {'this': 'is', 'a': 'dict'},
            123
        ]
        for results in test_results:
            audit_log.set_results(results)
            extras = audit_log._get_extras(log_type='test')
            self.assertIn('results', extras)
            self.assertEqual(extras['results'], results)

    def test_extras_logtype(self):
        audit_log = AuditLogger()
        extras = audit_log._get_extras(log_type='test_type')
        self.assertEqual(extras['type'], 'test_type')

    @patch('audit_log.logger.logger')
    def test_send_log_info(self, mocked_audit_logger):
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

        audit_log = AuditLogger()
        audit_log.info("message").send_log()
        mocked_audit_logger.log.assert_called_with(
            level=logging.INFO,
            msg='message',
            extra=extected_extra
        )

        # with self.assertLogs(logger=AUDIT_LOGGER_NAME) as mocked_logger:
        #     audit_log.info("message").send_log()
        #     self.assertEqual(mocked_logger.output, expected_log_output)
