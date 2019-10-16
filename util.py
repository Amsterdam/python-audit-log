import logging


def get_client_ip(request):
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    except Exception:
        logger = logging.getLogger(__name__)
        logger.warning('Failed to get ip for audit log', exc_info=True)
        return 'failed to get ip'
