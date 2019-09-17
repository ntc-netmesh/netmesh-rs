import requests
import json
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from netmesh_api.models import Server
from netmesh_api.models import Speedtest
from netmesh_api.models import IPaddress


class SubmitSpeedtestData(APIView):
    renderer_classes = (JSONRenderer,)

    def post(self, request):

        try:
            server = Server.objects.get(uuid__exact=request.data['server'])
        except Exception as e:  # TODO: find specific exception
            print(e)
            return Response("ERROR: Invalid server id",
                            status=status.HTTP_400_BAD_REQUEST)

        # extract addtl info from IP address
        ip_add = request.data['ip_address']
        # ip_add = '202.90.132.53'
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

        try:
            sp = Speedtest()
            sp.test_id = request.data['test_id']
            sp.sid = request.data['sid']
            sp.ip_address = ip
            sp.server = server
            sp.rtt_ave = request.data['result']['rttAve']
            sp.rtt_min = request.data['result']['rttMin']
            sp.rtt_max = request.data['result']['rttMax']
            sp.upload_speed = request.data['result']['ul']
            sp.download_speed = request.data['result']['dl']
            sp.save()
        except Exception as e:  # TODO: find specific exception
            print(e)
            return Response("ERROR: Data Save Failure",
                            status=status.HTTP_400_BAD_REQUEST)

        return Response("OK", status=status.HTTP_200_OK)
