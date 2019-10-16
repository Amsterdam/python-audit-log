from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

AUDIT_LOG_APP_NAME = getattr(settings, 'AUDIT_LOG_APP_NAME', None)

if not AUDIT_LOG_APP_NAME:
    raise ImproperlyConfigured('AUDIT_LOG_APP_NAME must be configured in settings')

AUDIT_LOG_LOGGER_NAME = 'audit_log'
