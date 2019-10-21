import logging
from unittest import TestCase
from unittest.mock import patch

from audit_log.logger import AuditLogger


class TestAuditlogger(TestCase):

    def test_default_log_level(self):
        auditlog = AuditLogger()
        self.assertEqual(auditlog.level, logging.INFO)
        self.assertEqual(auditlog.message, '')
        self.assertIsNone(auditlog.app)
        self.assertIsNone(auditlog.http_request)
        self.assertIsNone(auditlog.http_response)
        self.assertIsNone(auditlog.user)
        self.assertIsNone(auditlog.filter)
        self.assertIsNone(auditlog.results)

    def test_debug(self):
        auditlog = AuditLogger()
        auditlog.debug('test')
        self.assertEqual(auditlog.level, logging.DEBUG)
        self.assertEqual(auditlog.message, 'test')

    def test_info(self):
        auditlog = AuditLogger()
        auditlog.info('test')
        self.assertEqual(auditlog.level, logging.INFO)
        self.assertEqual(auditlog.message, 'test')

    def test_warning(self):
        auditlog = AuditLogger()
        auditlog.warning('test')
        self.assertEqual(auditlog.level, logging.WARNING)
        self.assertEqual(auditlog.message, 'test')

    def test_error(self):
        auditlog = AuditLogger()
        auditlog.error('test')
        self.assertEqual(auditlog.level, logging.ERROR)
        self.assertEqual(auditlog.message, 'test')

    def test_critical(self):
        auditlog = AuditLogger()
        auditlog.critical('test')
        self.assertEqual(auditlog.level, logging.CRITICAL)
        self.assertEqual(auditlog.message, 'test')

    def test_set_app_name(self):
        log = AuditLogger()
        log.set_app_name('test')
        self.assertEqual(log.app['name'], 'test')

    def test_set_http_request(self):
        auditlog = AuditLogger()
        auditlog.set_http_request(method='GET', url='http://localhost/', user_agent='test_agent')

        self.assertEqual(auditlog.http_request['method'], 'GET')
        self.assertEqual(auditlog.http_request['url'], 'http://localhost/')
        self.assertEqual(auditlog.http_request['user_agent'], 'test_agent')

    def test_set_http_response(self):
        auditlog = AuditLogger()
        auditlog.set_http_response(status_code=200, reason='OK', headers={'Test': 'test'})

        self.assertEqual(auditlog.http_response['status_code'], 200)
        self.assertEqual(auditlog.http_response['reason'], 'OK')
        self.assertEqual(auditlog.http_response['headers']['Test'], 'test')

    def test_set_user(self):
        auditlog = AuditLogger()
        auditlog.set_user(
            authenticated=True, provider='test', email='username@host.com',
            roles=['role1', 'role2'], ip='12.23.34.45', realm='testrealm'
        )

        self.assertEqual(auditlog.user['authenticated'], True)
        self.assertEqual(auditlog.user['provider']['name'], 'test')
        self.assertEqual(auditlog.user['provider']['realm'], 'testrealm')
        self.assertEqual(auditlog.user['email'], 'username@host.com')
        self.assertEqual(auditlog.user['roles'], ['role1', 'role2'])
        self.assertEqual(auditlog.user['ip'], '12.23.34.45')

    def test_set_filter(self):
        auditlog = AuditLogger()
        auditlog.set_filter(object_name='objname', fields='fields', terms='terms')
        self.assertEqual(auditlog.filter['object'], 'objname')
        self.assertEqual(auditlog.filter['fields'], 'fields')
        self.assertEqual(auditlog.filter['terms'], 'terms')

    def test_set_results(self):
        auditlog = AuditLogger()
        test_results = [
            'There are the results',
            ['this', 'is', 'a', 'list'],
            {'this': 'is', 'a': 'dict'},
            123
        ]
        for results in test_results:
            auditlog.set_results(results)
            self.assertEqual(auditlog.results, results)

    def test_extras_app_name(self):
        auditlog = AuditLogger()
        auditlog.set_app_name('test')

        extras = auditlog._get_extras(log_type='test')
        self.assertIn('app', extras)
        self.assertEqual(extras['app']['name'], 'test')

    def test_extras_http_request(self):
        auditlog = AuditLogger()
        auditlog.set_http_request(method='GET', url='http://localhost/', user_agent='test_agent')

        extras = auditlog._get_extras(log_type='test')
        self.assertIn('http_request', extras)
        self.assertEqual(extras['http_request']['method'], 'GET')
        self.assertEqual(extras['http_request']['url'], 'http://localhost/')
        self.assertEqual(extras['http_request']['user_agent'], 'test_agent')

    def test_extras_http_response(self):
        auditlog = AuditLogger()
        auditlog.set_http_response(status_code=200, reason='OK', headers={'Test': 'test'})

        extras = auditlog._get_extras(log_type='test')
        self.assertIn('http_response', extras)
        self.assertEqual(extras['http_response']['status_code'], 200)
        self.assertEqual(extras['http_response']['reason'], 'OK')
        self.assertEqual(extras['http_response']['headers']['Test'], 'test')

    def test_extras_user(self):
        auditlog = AuditLogger()
        auditlog.set_user(
            authenticated=True, provider='test', email='username@host.com',
            roles=['role1', 'role2'], ip='12.23.34.45', realm='testrealm'
        )

        extras = auditlog._get_extras(log_type='test')
        self.assertIn('user', extras)
        self.assertEqual(extras['user']['authenticated'], True)
        self.assertEqual(extras['user']['provider']['name'], 'test')
        self.assertEqual(extras['user']['provider']['realm'], 'testrealm')
        self.assertEqual(extras['user']['email'], 'username@host.com')
        self.assertEqual(extras['user']['roles'], ['role1', 'role2'])
        self.assertEqual(extras['user']['ip'], '12.23.34.45')

    def test_extras_filter(self):
        auditlog = AuditLogger()
        auditlog.set_filter(object_name='objname', fields='fields', terms='terms')

        extras = auditlog._get_extras(log_type='test')
        self.assertIn('filter', extras)
        self.assertEqual(extras['filter']['object'], 'objname')
        self.assertEqual(extras['filter']['fields'], 'fields')
        self.assertEqual(extras['filter']['terms'], 'terms')

    def test_extras_results(self):
        auditlog = AuditLogger()
        test_results = [
            'There are the results',
            ['this', 'is', 'a', 'list'],
            {'this': 'is', 'a': 'dict'},
            123
        ]
        for results in test_results:
            auditlog.set_results(results)
            extras = auditlog._get_extras(log_type='test')
            self.assertIn('results', extras)
            self.assertEqual(extras['results'], results)

    def test_extras_logtype(self):
        auditlog = AuditLogger()
        extras = auditlog._get_extras(log_type='test_type')
        self.assertEqual(extras['type'], 'test_type')

    @patch('audit_log.logger.audit_logger')
    def test_send_log_info(self, mocked_audit_logger):
        extected_extra = {'audit': {
                'app': None,
                'http_request': None,
                'http_response': None,
                'user': None,
                'filter': None,
                'results': None,
                'type': 'INFO'
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
        #     auditlog.info("message").send_log()
        #     self.assertEqual(mocked_logger.output, expected_log_output)
