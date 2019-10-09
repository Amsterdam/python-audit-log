from django.utils.deprecation import MiddlewareMixin

from audit_log import app_settings
from audit_log.log.logger import AuditLog


class AuditLogMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if not hasattr(request, 'audit_log'):
            request.audit_log = AuditLog()
            request.audit_log\
                .set_app_name(app_settings.AUDIT_LOG_APP_NAME)\
                .set_http_request(request)\
                .set_user_fom_request(request)

    def process_response(self, request, response):
        if hasattr(request, 'audit_log'):
            request.audit_log.set_http_response(response).send_log()
        return response
