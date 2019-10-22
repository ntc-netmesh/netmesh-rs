from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from netmesh_api.models import AgentProfile
from netmesh_api.models import UserProfile
from netmesh_api.models import DataPoint
from netmesh_api.models import Server
from netmesh_api.models import Test
from netmesh_api.models import RFC6349TestDevice
from netmesh_api.models import Traceroute, Hop
from netmesh_api.serializers import ServerSerializer
from netmesh_api.utils import get_client_ip
from netmesh_api.utils import get_isp
from netmesh_api.validators import check_lat, check_long


class SubmitData(APIView):
    """ Submit measurement data
        <base_url>/api/submit/?
    """
    renderer_classes = (JSONRenderer,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """ POST method for submitting a report """
        report = request.data
        user = request.user
        hash = request.data["hash"]

        if len(hash) != 64:
            return Response('ERROR: Invalid hash', status=status.HTTP_400_BAD_REQUEST)

        try:
            device = RFC6349TestDevice.objects.get(hash=hash)
        except ObjectDoesNotExist:
            return Response('ERROR: Invalid hash', status=status.HTTP_400_BAD_REQUEST)
        try:
            agent = AgentProfile.objects.get(user=user)
        except ObjectDoesNotExist as e:
            print(e)
            return Response("ERROR: Invalid Agent ID",
                            status=status.HTTP_400_BAD_REQUEST)

        ip_add = get_client_ip(request)
        ip = get_isp(ip_add)

        try:
            test = Test()
            test.agent = agent
            test.test_type = report["test_type"]
            test.network_connection = report["network"]
            test.pcap = report["pcap"]
            test.ip_address = ip
            test.lat = check_lat(report["lat"])
            test.long = check_long(report["long"])
            test.mode = report["mode"]
            test.device = device
            test.save()
            measurements = report["results"]
        except Exception as e:  # TODO: find specific exception
            return Response("ERROR: Data Save Failure, %s" % e,
                            status=status.HTTP_400_BAD_REQUEST)

        for dataset in measurements:
            # test first if server id in payload is valid
            try:
                server = Server.objects.get(uuid=measurements[dataset]["server"])
            except ObjectDoesNotExist:
                return Response("ERROR: Invalid Server ID",
                                status=status.HTTP_400_BAD_REQUEST)
            new_data = DataPoint()
            new_data.test_id = test
            new_data.date_tested = measurements[dataset]["ts"]
            new_data.direction = measurements[dataset]["direction"]
            new_data.server = server
            new_data.path_mtu = measurements[dataset]["path_mtu"]
            new_data.baseline_rtt = measurements[dataset]["baseline_rtt"]
            new_data.bottleneck_bw = measurements[dataset]["bottleneck_bw"]
            new_data.bdp = measurements[dataset]["bdp"]
            new_data.min_rwnd = measurements[dataset]["min_rwnd"]
            new_data.ave_tcp_tput = measurements[dataset]["ave_tcp_tput"]
            new_data.ideal_tcp_tput = measurements[dataset]["ideal_tcp_tput"]
            new_data.actual_transfer_time = measurements[dataset]["actual_transfer_time"]
            new_data.ideal_transfer_time = measurements[dataset]["ideal_transfer_time"]
            new_data.tcp_ttr = measurements[dataset]["tcp_ttr"]
            new_data.trans_bytes = measurements[dataset]["trans_bytes"]
            new_data.retrans_bytes = measurements[dataset]["retrans_bytes"]
            new_data.tcp_eff = measurements[dataset]["tcp_eff"]
            new_data.ave_rtt = measurements[dataset]["ave_rtt"]
            new_data.buffer_delay = measurements[dataset]["buffer_delay"]
            new_data.save()

        return Response('OK CREATED', status=status.HTTP_200_OK)


class RegisterClientDevice(APIView):
    """ API endpoint to register a client device
        <base_url>/api/register/?
    """
    renderer_classes = (JSONRenderer,)
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        username = request.user
        hash = request.data["hash"]

        try:
            user = UserProfile.objects.get(user__username=username)
        except ObjectDoesNotExist:
            return Response('ERROR: User does not exist', status=status.HTTP_404_NOT_FOUND)

        if user in AgentProfile.objects.all():
            return Response('ERROR: User not authorized', status=status.HTTP_401_UNAUTHORIZED)

        if len(hash) != 64:
            return Response('ERROR: Invalid hash', status=status.HTTP_400_BAD_REQUEST)

        try:
            # try to save device uuid hash
            device = RFC6349TestDevice()
            device.created_by = user
            device.hash = hash
            device.save()
            return Response('SUCCESS', status=status.HTTP_200_OK)
        except IntegrityError:
            # hash is not unique!
            return Response('ERROR: Hash already exists', status=status.HTTP_400_BAD_REQUEST)


class GetToken(APIView):
    """ API endpoint to get Agent token
        <base_url>/api/gettoken/?
    """
    renderer_classes = (JSONRenderer,)
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        hash = request.data["hash"]

        if len(hash) != 64:
            return Response('ERROR: Invalid hash', status=status.HTTP_400_BAD_REQUEST)

        try:
            device = RFC6349TestDevice.objects.get(hash=hash)
        except ObjectDoesNotExist:
            return Response('ERROR: Invalid hash', status=status.HTTP_400_BAD_REQUEST)

        try:
            AgentProfile.objects.get(user=user)
        except ObjectDoesNotExist:
            return Response("ERROR: Invalid Agent ID", status=status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({'Token': token.key},
                        status=status.HTTP_200_OK)


class ServerViewSet(viewsets.ReadOnlyModelViewSet):
    """
        API endpoint to retrieve list of servers
        <base_url>/api/servers/?
    """
    renderer_classes = (JSONRenderer,)

    queryset = Server.objects.all().order_by('pk')
    serializer_class = ServerSerializer


class SubmitTraceroute(APIView):
    """ Submit traceroute data
            <base_url>/api/submit/?
        """
    renderer_classes = (JSONRenderer,)

    def post(self, request):

        traceroute = request.data
        try:
            tr = Traceroute()
            tr.origin_ip = get_client_ip(request)
            tr.dest_ip = traceroute["dest_ip"]
            tr.dest_name = traceroute["dest_name"]
            tr.save()
        except Exception as e:  # TODO: find specific exception
            print(e)
            return Response("ERROR: Data Save Failure",
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            for index in traceroute["hops"]:
                newhop = Hop()
                newhop.traceroute = tr
                newhop.hop_index = index
                newhop.host_ip = traceroute["hops"][index]["hostip"]
                newhop.host_name = traceroute["hops"][index]["hostname"]
                newhop.time1 = traceroute["hops"][index]["t1"]
                newhop.time2 = traceroute["hops"][index]["t2"]
                newhop.time3 = traceroute["hops"][index]["t3"]
                newhop.save()
        except Exception as e:  # TODO: find specific exception
            print(e)
            return Response("ERROR: Data Save Failure",
                            status=status.HTTP_400_BAD_REQUEST)

        return Response("OK", status=status.HTTP_200_OK)

