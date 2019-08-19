from django.test import TestCase
from netmesh_api import models
import random
import json
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient



def random_ip():
    ip = "%s.%s.%s.%s" % (
        random.randint(1, 255), random.randint(1, 255),
        random.randint(1, 255), random.randint(1, 255))
    return ip

def random_traceroute():
    data = {
        "dest_ip": random_ip(),
        "dest_name": "randoom.dest.name",
        "hops": {
            "1": {
                "hostip": random_ip(),
                "hostname": "another.dummy.domain",
                "t1": random.uniform(1, 1000),
                "t2": random.uniform(1, 1000),
                "t3": random.uniform(1, 1000)
            },
            "2": {
                "hostip": random_ip(),
                "hostname": "local.pinas.com",
                "t1": random.uniform(1, 1000),
                "t2": random.uniform(1, 1000),
                "t3": random.uniform(1, 1000)
            }
        }
    }
    return data

class TracerouteTestCase(TestCase):

    def test_register(self):
        """ We should be able to submit a normal traceroute data payload"""

        self.assertEqual(0, models.Traceroute.objects.all().count())

        url = '/api/submit/traceroute'
        client = APIClient()
        response = client.post(url, data=random_traceroute(), format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.data)
        self.assertEqual(1, models.Traceroute.objects.all().count())