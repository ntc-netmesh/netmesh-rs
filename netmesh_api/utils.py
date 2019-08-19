import iso8601
import subprocess
from django.utils import timezone

from netmesh_api import choices


def check_timestamp(ts):
    try:
        return iso8601.parse_date(ts)
    except:
        return timezone.now()


def check_connection_type(conn):
    if conn not in choices.network_choices:
        return 'unknown'
    else:
        return conn


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
