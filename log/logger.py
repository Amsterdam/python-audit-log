import logging

from audit_log.log import audit_logger
from audit_log.log.base import BaseLog
from audit_log.util import get_client_ip


class AuditLog(BaseLog):
    app = None
    http_request = None
    http_response = None
    user = None
    filter = None
    results = None

    def set_app_name(self, name):
        self.app = {
            'name': name,
        }
        return self

    def set_http_request(self, request):
        self.http_request = {
            'method': request.method,
            'url': request.build_absolute_uri(),
            'user_agent': request.META.get('HTTP_USER_AGENT', '?') if request.META else '?'
        }
        return self

    def set_http_response(self, response):
        headers = response.serialize_headers().decode('ascii') \
            if hasattr(response, 'serialize_headers') and callable(getattr(response, 'serialize_headers')) \
            else ''

        headers = {header.split(':', 1)[0].strip(): header.split(':', 1)[1].strip() for header in
                   headers.split('\r\n')}
        self.http_response = {
            'status_code': getattr(response, 'status_code', ''),
            'reason': getattr(response, 'reason_phrase', ''),
            'headers': headers
        }
        return self

    def set_user_fom_request(self, request, realm=''):
        roles = list(request.user.groups.values_list('name', flat=True)) if request.user else []
        self.set_user(
            authenticated=request.user.is_authenticated if request.user else False,
            provider=request.session.get('_auth_user_backend', ''),
            realm=realm,
            email=getattr(request.user, 'email', ''),
            roles=roles,
            ip=get_client_ip(request)
        )
        return self

    def set_user(self, authenticated, provider, email, roles, ip, realm=""):
        self.user = {
            'authenticated': authenticated,
            'email': email,
            'roles': roles,
            'ip': ip,
            'provider': {
                'name': provider,
                'realm': realm,
            }
        }
        return self

    def set_filter(self, object_name, fields, terms):
        self.filter = {
            'object': object_name,
            'fields': fields,
            'terms': terms
        }
        return self

    def set_results(self, results):
        self.results = results
        return self

    def get_extras(self, log_type):
        return {
            'app': self.app,
            'http_request': self.http_request,
            'http_response': self.http_response,
            'user': self.user,
            'filter': self.filter,
            'results': self.results,
            'type': log_type
        }

    def send_log(self):
        audit_logger.log(
            self.level,
            self.message,
            extra=self.get_extras(logging.getLevelName(self.level)))
