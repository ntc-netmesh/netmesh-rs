import ast
import json
import json
import pytz
import random
import random
import requests
import requests
import uuid
from datetime import datetime
from django.test import TestCase
from mock import Mock
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from rest_framework.test import APIRequestFactory

from netmesh_api import models
from netmesh_api.tests.utils import random_ip


class RFC6349TestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        cls.username = "agent1"
        cls.password = "6ff98bf9d"
        cls.agent = models.User(username=cls.username, password=cls.password)
        cls.agent.save()
        cls.token, _ = Token.objects.get_or_create(user=cls.agent)
        print(cls.token)

        # create dummy agentprofile
        cls.agentprofile = models.AgentProfile(user=cls.agent)
        cls.agentprofile.save()
        cls.uuid = cls.agentprofile.uuid

        cls.server = models.Server()
        cls.server.nickname = "test server"
        cls.server.ip_address = random_ip()
        cls.server.type = "rfc-6349"
        cls.server.lat = 16.647322
        cls.server.long = 121.071959
        cls.server.city = "Quezon City"
        cls.server.province = "NCR"
        cls.server.country = "Philippines"
        cls.server.sponsor = "Dummy Org"
        cls.server.hostname = "http://dummyhostname.com"
        cls.server.save()

    def setUp(cls):
        cls.data_point = {
            "uuid": cls.uuid,
            "test_type": "RFC6349",
            "network": "dsl",
            "pcap": "sample.pcap",
            "lat": random.uniform(12, 13),
            "long": random.uniform(121, 123),
            "mode": random.choices(['normal', 'reverse', 'bidirectional', 'simultaneous'])[0],
            "results": {
                "set1": {
                    "ts": pytz.utc.localize(datetime.utcnow()),
                    "server": cls.server.uuid,
                    "direction": random.choices(['forward', 'reverse'])[0],
                    "path_mtu": random.randint(1400, 1500),
                    "baseline_rtt": random.uniform(1, 1000),
                    "bottleneck_bw": random.uniform(1, 10000000000),
                    "bdp": random.uniform(1, 10000000000),
                    "min_rwnd": random.uniform(1, 65000),
                    "ave_tcp_tput": random.uniform(1, 10000000000),
                    "ideal_tcp_tput": random.uniform(1, 10000000000),
                    "actual_transfer_time": random.uniform(1, 100),
                    "ideal_transfer_time": random.uniform(1, 100),
                    "tcp_ttr": random.uniform(0, 1),
                    "trans_bytes": random.uniform(1, 10000000000),
                    "retrans_bytes": random.uniform(1, 10000000000),
                    "tcp_eff": random.uniform(1, 100),
                    "ave_rtt": random.uniform(1, 1000),
                    "buffer_delay": random.uniform(1, 10000000000),
                },
                "set2": {
                    "ts": pytz.utc.localize(datetime.utcnow()),
                    "server": cls.server.uuid,
                    "direction": random.choices(['forward', 'reverse'])[0],
                    "path_mtu": random.randint(1400, 1500),
                    "baseline_rtt": random.uniform(1, 1000),
                    "bottleneck_bw": random.uniform(1, 10000000000),
                    "bdp": random.uniform(1, 10000000000),
                    "min_rwnd": random.uniform(1, 65000),
                    "ave_tcp_tput": random.uniform(1, 10000000000),
                    "ideal_tcp_tput": random.uniform(1, 10000000000),
                    "actual_transfer_time": random.uniform(1, 100),
                    "ideal_transfer_time": random.uniform(1, 100),
                    "tcp_ttr": random.uniform(0, 1),
                    "trans_bytes": random.uniform(1, 10000000000),
                    "retrans_bytes": random.uniform(1, 10000000000),
                    "tcp_eff": random.uniform(1, 100),
                    "ave_rtt": random.uniform(1, 1000),
                    "buffer_delay": random.uniform(1, 10000000000),
                },
            }
        }
        cls.data_json = json.dumps(cls.data_point, default=str)
        cls.status_len = str(len(cls.data_json))

    @classmethod
    def tearDownClass(cls):
        cls.server.delete()
        cls.agentprofile.delete()
        cls.agent.delete()

    def test_submit_normal(self):
        """ We should be able to submit a normal data payload"""
        self.assertEqual(0, models.Test.objects.all().count())
        self.assertEqual(0, models.DataPoint.objects.all().count())

        url = '/api/submit'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.agent.auth_token.key)
        response = self.client.post(url, data=self.data_point, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual('OK CREATED', response.data)
        self.assertEqual(1, models.Test.objects.all().count())
        self.assertEqual(2, models.DataPoint.objects.all().count())

    def test_submit_no_token(self):
        """ Submitting without tokens should fail """
        self.assertEqual(0, models.Test.objects.all().count())
        self.assertEqual(0, models.DataPoint.objects.all().count())

        url = '/api/submit'
        response = self.client.post(url, data=self.data_point, format='json')

        self.assertEqual(401, response.status_code)
        self.assertEqual(0, models.Test.objects.all().count())
        self.assertEqual(0, models.DataPoint.objects.all().count())

    def test_malformed_agent_uuid(self):
        """ Requests with missing or invalid agent uuids should fail """
        self.assertEqual(0, models.Test.objects.all().count())
        self.assertEqual(0, models.DataPoint.objects.all().count())

        self.data_point['uuid'] = 'bad uuid'
        url = '/api/submit'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.agent.auth_token.key)
        response = self.client.post(url, data=self.data_point, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual('ERROR: Malformed UUID', response.data)
        self.assertEqual(0, models.Test.objects.all().count())
        self.assertEqual(0, models.DataPoint.objects.all().count())

    def test_empty_agent_uuid(self):
        """ Requests with missing or invalid agent uuids should fail """
        self.assertEqual(0, models.Test.objects.all().count())
        self.assertEqual(0, models.DataPoint.objects.all().count())

        self.data_point['uuid'] = ""
        url = '/api/submit'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.agent.auth_token.key)
        response = self.client.post(url, data=self.data_point, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual('ERROR: Malformed UUID', response.data)
        self.assertEqual(0, models.Test.objects.all().count())
        self.assertEqual(0, models.DataPoint.objects.all().count())

    def test_well_formed_but_invalid_agent_uuid(self):
        """ Requests with missing or invalid agent uuids should fail """
        self.assertEqual(0, models.Test.objects.all().count())
        self.assertEqual(0, models.DataPoint.objects.all().count())

        self.data_point['uuid'] = uuid.uuid4()
        url = '/api/submit'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.agent.auth_token.key)
        response = self.client.post(url, data=self.data_point, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual('ERROR: Invalid Agent ID', response.data)
        self.assertEqual(0, models.Test.objects.all().count())
        self.assertEqual(0, models.DataPoint.objects.all().count())
