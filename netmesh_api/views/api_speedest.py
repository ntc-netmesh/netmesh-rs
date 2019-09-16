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

from netmesh_api.models import Speedtest
from netmesh_api.models import Server


class SubmitSpeedtestData(APIView):
    renderer_classes = (JSONRenderer,)

    def post(self, request):

        try:
            server = Server.objects.get(uuid__exact=request.data['server'])
        except Exception as e:  # TODO: find specific exception
            print(e)
            return Response("ERROR: Invalid server id",
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            sp = Speedtest()
            sp.test_id = request.data['test_id']
            sp.sid = request.data['sid']
            sp.ip_address = request.data['ip_address']
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