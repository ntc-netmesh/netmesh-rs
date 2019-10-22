import iso8601
import json
import requests
import subprocess
from django.utils import timezone

from netmesh_api import choices
from netmesh_api.models import IPaddress


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


def get_isp(ip_add):
    fields = "?fields=status,message,country,countryCode,region,regionName,city,zip," \
             "lat,lon,timezone,isp,org,as,asname,reverse,mobile,proxy,query"
    base_url = "http://ip-api.com/json/"
    url = base_url + ip_add + fields

    try:
        response = requests.get(url, timeout=30)
        ip_data = json.loads(response.text)
        req_status = ip_data['status']
    except:
        req_status = 'failed'  # we explicity declare that it failed due to network connection issues, etc

    try:
        # TODO: handle updates in databases (i.e. IP address has now new ISP or ownwer)
        ip = IPaddress.objects.get(ip_address=ip_add)
    except IPaddress.DoesNotExist:  # so let's create a new entry
        ip = IPaddress()
        ip.ip_address = ip_add
        ip.save()
        if req_status == 'success':
            ip.country = ip_data['country']
            ip.country_code = ip_data['countryCode']
            ip.region = ip_data['region']
            ip.region_name = ip_data['regionName']
            ip.city = ip_data['city']
            ip.zip = ip_data['zip']
            ip.lat = ip_data['lat']
            ip.long = ip_data['lon']
            ip.timezone = ip_data['timezone']
            ip.isp = ip_data['isp']
            ip.org = ip_data['org']
            ip.as_name = ip_data['asname']
            ip.as_num = ip_data['as']
            ip.reverse = ip_data['reverse']
            ip.mobile = ip_data['mobile']
            ip.proxy = ip_data['proxy']
            ip.save()

    return ip
