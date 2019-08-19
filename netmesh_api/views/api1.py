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

from netmesh_api.models import AgentProfile
from netmesh_api.models import DataPoint
from netmesh_api.models import Server
from netmesh_api.models import Test
from netmesh_api.models import Traceroute, Hop
from netmesh_api.serializers import ServerSerializer
from netmesh_api.utils import get_client_ip


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

        try:
            agent = AgentProfile.objects.get(uuid=report["uuid"])
        except ObjectDoesNotExist:
            return Response("ERROR: Invalid Agent ID",
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            test = Test()
            test.agent = agent
            test.test_type = report["test_type"]
            test.network_connection = report["network"]
            test.pcap = report["pcap"]
            test.ip_address = get_client_ip(request)
            test.lat = report["lat"]
            test.long = report["long"]
            test.mode = report["mode"]
            test.save()
            measurements = report["results"]
        except Exception:  # TODO: find specific exception
            return Response("ERROR: Data Save Failure",
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


class Register(APIView):
    """ API endpoint to get Agent token
        <base_url>/api/register/?
    """
    renderer_classes = (JSONRenderer,)

    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        uuid = request.data["uuid"]

        try:
            AgentProfile.objects.get(uuid=uuid)
        except ObjectDoesNotExist:
            return Response("ERROR: Invalid Agent ID", status=status.HTTP_400_BAD_REQUEST)

        if username is None or password is None:
            return Response({'ERROR': 'Please provide both username and password'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if not user:
            return Response({'ERROR': 'Invalid Credentials'}, status=status.HTTP_404_NOT_FOUND)

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

