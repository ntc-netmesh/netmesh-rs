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


class SubmitSpeedtestData(APIView):
    renderer_classes = (JSONRenderer,)

    def post(self, request):

        try:
            sp = Speedtest()
            sp.test_id = request.data['test_id']
            sp.sid = request.data['sid']
            sp.ip_address = request.data['ip_address']
            sp.rtt = request.data['rtt']
            sp.upload_speed = request.data['ul']
            sp.download_speed = request.data['dl']
            sp.save()
        except Exception as e:  # TODO: find specific exception
            print(e)
            return Response("ERROR: Data Save Failure",
                            status=status.HTTP_400_BAD_REQUEST)

        return Response("OK", status=status.HTTP_200_OK)