from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import (TokenAuthentication,
                                           SessionAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from django.core.exceptions import ObjectDoesNotExist

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
        test.network_connection = report["network_connection"]
        test.pcap = report["pcap"]
        test.ip_address = self.get_client_ip(request)
        test.save()
        measurements = report["results"]

        for dataset in measurements:
            new_data = DataPoint()
            new_data.date_tested = measurements[dataset]["ts"]
            new_data.rtt = measurements[dataset]["rtt"]
            new_data.upload_speed = measurements[dataset]["upload"]
            new_data.download_speed = measurements[dataset]["download"]
            new_data.test_id = test.pk
            new_data.save()

        return Response('OK CREATED', status=status.HTTP_200_OK)
