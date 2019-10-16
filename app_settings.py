from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

AUDIT_LOG_APP_NAME = getattr(settings, 'AUDIT_LOG_APP_NAME', None)
AUDIT_LOG_LOGSTASH_HOST = getattr(settings, 'AUDIT_LOG_LOGSTASH_HOST', None)
AUDIT_LOG_LOGSTASH_PORT = getattr(settings, 'AUDIT_LOG_LOGSTASH_PORT', None)

if not AUDIT_LOG_APP_NAME:
    raise ImproperlyConfigured('AUDIT_LOG_APP_NAME must be configured in settings')
if not AUDIT_LOG_LOGSTASH_HOST:
    raise ImproperlyConfigured('AUDIT_LOG_LOGSTASH_HOST must be configured in settings')
if not AUDIT_LOG_LOGSTASH_PORT:
    raise ImproperlyConfigured('AUDIT_LOG_LOGSTASH_PORT must be configured in settings')

# Ensure port is an integer
AUDIT_LOG_LOGSTASH_PORT = int(AUDIT_LOG_LOGSTASH_PORT)

AUDIT_LOG_LOGGER_NAME = 'audit_log'
