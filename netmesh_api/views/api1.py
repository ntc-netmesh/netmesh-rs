from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import (TokenAuthentication,
                                           SessionAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate

from django.utils import timezone as timezone

from netmesh_api.models import Test
from netmesh_api.models import DataPoint
from netmesh_api.models import Server
from netmesh_api.models import AgentProfile


class SubmitData(APIView):
    """ Submit measurement data
        <base_url>/api/submit/?
    """
    renderer_classes = (JSONRenderer,)

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        """ POST method for submitting a report """
        report = request.data

        try:
            agent = AgentProfile.objects.get(uuid=report["uuid"])
        except ObjectDoesNotExist:
            return Response("ERROR: Invalid Agent ID",
                            status=status.HTTP_401_UNAUTHORIZED)

        test = Test()
        test.agent = agent
        test.test_type = report["test_type"]
        test.network_connection = report["network"]
        test.pcap = report["pcap"]
        test.ip_address = self.get_client_ip(request)
        test.save()
        measurements = report["results"]

        for dataset in measurements:
            new_data = DataPoint()
            new_data.server = Server.objects.get(uuid=measurements[dataset]["server"])
            new_data.date_tested = measurements[dataset]["ts"]
            new_data.rtt = measurements[dataset]["rtt"]
            new_data.upload_speed = measurements[dataset]["upload"]
            new_data.download_speed = measurements[dataset]["download"]
            new_data.test_id = test
            new_data.save()

        return Response('OK CREATED', status=status.HTTP_200_OK)


class Register(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        uuid = request.data.get("uuid")

        try:
            AgentProfile.objects.get(uuid=uuid)
        except ObjectDoesNotExist:
            return Response("ERROR: Invalid Agent ID",
                                status=status.HTTP_400_BAD_REQUEST)


        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'},
                            status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=status.HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key},
                        status=status.HTTP_200_OK)