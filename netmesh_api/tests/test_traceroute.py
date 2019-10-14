from django.test import TransactionTestCase
from netmesh_api import models
import random
import json
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient

from netmesh_api.tests.utils import random_ip


def generate_traceroute():
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


class TracerouteTestCase(TransactionTestCase):

    def test_normal_submit(self):
        """ We should be able to submit a normal traceroute data payload"""
        self.assertEqual(0, models.Traceroute.objects.all().count())
        self.assertEqual(0, models.Hop.objects.all().count())
        tr = generate_traceroute()
        url = '/api/submit/traceroute'
        client = APIClient()
        response = client.post(url, data=tr, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.data)
        self.assertEqual(1, models.Traceroute.objects.all().count())
        self.assertEqual(2, models.Hop.objects.all().count())

    def test_missing_ip(self):
        """ If IP address is missing, API should return HTTP 400"""
        self.assertEqual(0, models.Traceroute.objects.all().count())
        self.assertEqual(0, models.Hop.objects.all().count())
        tr = generate_traceroute()
        tr['dest_ip'] = None
        url = '/api/submit/traceroute'
        client = APIClient()
        response = client.post(url, data=tr, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(0, models.Traceroute.objects.all().count())
        self.assertEqual(0, models.Hop.objects.all().count())

    def test_missing_dest_name(self):
        """ If destination hostname is missing, API should return HTTP 400"""
        self.assertEqual(0, models.Traceroute.objects.all().count())
        self.assertEqual(0, models.Hop.objects.all().count())
        tr = generate_traceroute()
        tr['dest_name'] = None
        url = '/api/submit/traceroute'
        client = APIClient()
        response = client.post(url, data=tr, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(0, models.Traceroute.objects.all().count())
        self.assertEqual(0, models.Hop.objects.all().count())

    def test_no_hop_info(self):
        """ Traceroute API should still succeed even if no Hop info is provided """
        self.assertEqual(0, models.Traceroute.objects.all().count())
        self.assertEqual(0, models.Hop.objects.all().count())
        tr = generate_traceroute()
        tr['hops'] = {}
        url = '/api/submit/traceroute'
        client = APIClient()
        response = client.post(url, data=tr, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, models.Traceroute.objects.all().count())
        self.assertEqual(0, models.Hop.objects.all().count())

    def test_null_times_for_hop_info(self):
        """ API will still accept even if time fields are empty"""
        self.assertEqual(0, models.Traceroute.objects.all().count())
        self.assertEqual(0, models.Hop.objects.all().count())
        tr = generate_traceroute()
        tr['hops']['1']['t1'] = None
        tr['hops']['1']['t2'] = None
        tr['hops']['1']['t3'] = None
        url = '/api/submit/traceroute'
        client = APIClient()
        response = client.post(url, data=tr, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, models.Traceroute.objects.all().count())
        self.assertEqual(2, models.Hop.objects.all().count())

    def test_empty_hop(self):
        """ Traceroute API should should return 400 if one of the hops is empty {}"""
        self.assertEqual(0, models.Traceroute.objects.all().count())
        self.assertEqual(0, models.Hop.objects.all().count())
        tr = generate_traceroute()
        tr['hops']['2'] = {}  # empty hop
        url = '/api/submit/traceroute'
        client = APIClient()
        response = client.post(url, data=tr, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(1, models.Traceroute.objects.all().count())
        self.assertEqual(1, models.Hop.objects.all().count())