import json
import random
import requests
import uuid
from django.test import TestCase
from mock import Mock
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory

from netmesh_api import models
from netmesh_api.tests.utils import random_ip


class SpeedtestTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server = models.Server()
        cls.server.nickname = "test server"
        cls.server.ip_address = random_ip()
        cls.server.type = "web-based"
        cls.server.lat = 16.647322
        cls.server.long = 121.071959
        cls.server.city = "Quezon City"
        cls.server.province = "NCR"
        cls.server.country = "Philippines"
        cls.server.sponsor = "Dummy Org"
        cls.server.hostname = "http://dummyhostname.com"
        cls.server.save()

    def setUp(cls):
        cls.speedtest_data = {
            "test_id": uuid.uuid4(),
            "sid": str(uuid.uuid4()).replace('-', ''),
            "ip_address": random_ip(),
            "result": {
                "rttAve": random.uniform(0, 10000),
                "rttMin": random.uniform(0, 10000),
                "rttMax": random.uniform(0, 10000),
                "ul": random.uniform(1, 10000000000),
                "dl": random.uniform(1, 10000000000),
            },
            "server": cls.server.uuid,
        }

        cls.fake_ip_data = '{"as":"AS9821 Advanced Science and Technology Institute",' \
                           '"asname":"LAIX-TRANSIT-CUST-AS9821",' \
                           '"city":"Batangas","country":"Philippines","countryCode":"PH",' \
                           '"isp":"Advanced Science and Technology Institute","lat":13.7594,"lon":121.06,' \
                           '"mobile":false,"org":"Advanced Science and Technology Institute",' \
                           '"proxy":false,"query":"202.90.132.53","region":"40",' \
                           '"regionName":"Calabarzon","reverse":"","status":"success",' \
                           '"timezone":"Asia/Manila","zip":"4200"}'

    @classmethod
    def tearDownClass(cls):
        cls.server.delete()

    def test_submit_normal(self):
        """ We should be able to submit a normal speedtest data payload"""
        requests.get = Mock(return_value=self.fake_ip_data)
        self.assertEqual(0, models.Speedtest.objects.all().count())
        self.assertEqual(0, models.IPaddress.objects.all().count())

        url = '/api/submit/speedtest'
        client = APIClient()
        response = client.post(url, data=self.speedtest_data, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.data)
        self.assertEqual(1, models.Speedtest.objects.all().count())
        self.assertEqual(1, models.IPaddress.objects.all().count())

    def test_no_IP_geolocation_data(self):
        """ If request to IP-API should fail, our API should still save the client (tester's) IP address
           All the other fields other than ip address is NULL
        """
        requests.get = Mock(return_value=None)
        self.assertEqual(0, models.Speedtest.objects.all().count())
        self.assertEqual(0, models.IPaddress.objects.all().count())

        url = '/api/submit/speedtest'
        client = APIClient()
        response = client.post(url, data=self.speedtest_data, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.data)
        self.assertEqual(1, models.Speedtest.objects.all().count())
        self.assertEqual(1, models.IPaddress.objects.all().count())

        ip_entry = models.IPaddress.objects.get(id=1)
        self.assertEqual(ip_entry.ip_address, self.speedtest_data['ip_address'])
        # check that other fields are the default values
        self.assertEqual(ip_entry.country, "")
        self.assertEqual(ip_entry.country_code, "")
        self.assertEqual(ip_entry.region, "")
        self.assertEqual(ip_entry.region_name, "")
        self.assertEqual(ip_entry.city, "")
        self.assertEqual(ip_entry.lat, 0)
        self.assertEqual(ip_entry.long, 0)
        self.assertEqual(ip_entry.timezone, "Asia/Manila")
        self.assertEqual(ip_entry.isp, "")
        self.assertEqual(ip_entry.org, "")
        self.assertEqual(ip_entry.as_num, "")
        self.assertEqual(ip_entry.mobile, False)
        self.assertEqual(ip_entry.proxy, False)

    def test_missing_server_id(self):
        """ This test should fail if there is no server uuid provided"""
        self.assertEqual(0, models.Speedtest.objects.all().count())
        self.assertEqual(0, models.IPaddress.objects.all().count())

        self.speedtest_data["server"] = ""
        url = '/api/submit/speedtest'
        client = APIClient()
        response = client.post(url, data=self.speedtest_data, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual('ERROR: Invalid server id', response.data)
        self.assertEqual(0, models.Speedtest.objects.all().count())
        self.assertEqual(0, models.IPaddress.objects.all().count())

    def test_missing_results_dict(self):
        """ Creating the speedtest object should fail if the results part are missing """
        requests.get = Mock(return_value=None)
        self.assertEqual(0, models.Speedtest.objects.all().count())
        self.assertEqual(0, models.IPaddress.objects.all().count())

        self.speedtest_data["result"] = {}
        url = '/api/submit/speedtest'
        client = APIClient()
        response = client.post(url, data=self.speedtest_data, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual('ERROR: Data Save Failure', response.data)
        self.assertEqual(0, models.Speedtest.objects.all().count())
        self.assertEqual(1, models.IPaddress.objects.all().count())
