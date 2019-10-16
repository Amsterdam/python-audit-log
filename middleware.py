from django.utils.deprecation import MiddlewareMixin

from audit_log import app_settings
from audit_log.log.logger import AuditLog


class AuditLogMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if not hasattr(request, 'audit_log'):
            audit_log = AuditLog()
            audit_log.set_app_name(app_settings.AUDIT_LOG_APP_NAME)
            audit_log.set_http_request(request)
            audit_log.set_user_from_request(request)
            request.audit_log = audit_log

    def process_response(self, request, response):
        if hasattr(request, 'audit_log'):
            audit_log = request.audit_log
            audit_log.set_http_response(response)
            audit_log.send_log()
        return response
