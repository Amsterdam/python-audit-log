import logging

from audit_log.log import audit_logger
from audit_log.log.base import BaseLog
from audit_log.util import get_client_ip


class AuditLog(BaseLog):

    def __init__(self) -> None:
        super().__init__()
        self.app = None
        self.http_request = None
        self.http_response = None
        self.user = None
        self.filter = None
        self.results = None

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
        headers = self._get_headers_from_response(response)
        self.http_response = {
            'status_code': getattr(response, 'status_code', ''),
            'reason': getattr(response, 'reason_phrase', ''),
            'headers': headers
        }
        return self

    def set_user_from_request(self, request, realm=''):
        user = request.user if hasattr(request, 'user') else None
        roles = list(user.groups.values_list('name', flat=True)) if user else []
        self.set_user(
            authenticated=user.is_authenticated if user else False,
            provider=request.session.get('_auth_user_backend', '') if hasattr(request, 'session') else '',
            realm=realm,
            email=getattr(user, 'email', '') if user else '',
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
            extra={'audit': self.get_extras(logging.getLevelName(self.level))})

    def _get_headers_from_response(self, response):
        return {header: value for header, value in response.items()}
