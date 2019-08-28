from django.test import TestCase
from netmesh_api import models
import random
import json
import uuid
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient


def random_ip():
    ip = "%s.%s.%s.%s" % (
        random.randint(1, 255), random.randint(1, 255),
        random.randint(1, 255), random.randint(1, 255))
    return ip


def random_speedtest():
    data = {
        "test_id": uuid.uuid4(),
        "sid": str(uuid.uuid4()).replace('-', ''),
        "ip_address": random_ip(),
        "rtt": random.uniform(0, 10000),
        "ul": random.uniform(1, 10000000000),
        "dl": random.uniform(1, 10000000000),
    }
    return data


class SpeedtestTestCase(TestCase):

    def test_submit_normal(self):
        """ We should be able to submit a normal speedtest data payload"""

        self.assertEqual(0, models.Speedtest.objects.all().count())

        url = '/api/submit/speedtest'
        client = APIClient()
        response = client.post(url, data=random_speedtest(), format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.data)
        self.assertEqual(1, models.Speedtest.objects.all().count())
