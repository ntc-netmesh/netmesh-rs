import ast
import base64
import json
import json
import pytz
import random
import random
import requests
import requests
import secrets
import uuid
from datetime import datetime
from django.test import TestCase
from mock import Mock
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from rest_framework.test import APIRequestFactory

from netmesh_api import models
from netmesh_api.tests.utils import random_ip


class RegisterTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        cls.username = "agent1"
        cls.staff_username = "staff1"
        cls.password = "6ff98bf9d"
        cls.agent = models.User(username=cls.username)
        cls.agent.set_password(cls.password)
        cls.agent.save()
        cls.staff = models.User(username=cls.staff_username)
        cls.staff.set_password(cls.password)
        cls.staff.save()
        cls.token, _ = Token.objects.get_or_create(user=cls.agent)

        # create dummy agentprofile
        cls.agentprofile = models.AgentProfile(user=cls.agent)
        cls.agentprofile.save()
        cls.uuid = cls.agentprofile.uuid
        cls.userprofile = models.UserProfile(user=cls.staff)
        cls.userprofile.save()

        # create RFC6349 test device
        cls.hash = secrets.token_hex(nbytes=32)

    def setUp(cls):
        cls.data_point = {
            "hash": cls.hash
        }
        cls.data_json = json.dumps(cls.data_point, default=str)
        cls.status_len = str(len(cls.data_json))

    @classmethod
    def tearDownClass(cls):
        cls.agentprofile.delete()
        cls.userprofile.delete()
        cls.agent.delete()
        cls.staff.delete()

    def test_register_normal(self):
        """ We should be able to register a device hash given correct credentials"""
        self.assertEqual(0, models.RFC6349TestDevice.objects.all().count())

        url = '/api/register'
        credentials = base64.b64encode(('%s:%s' % (self.staff_username, self.password)).encode()).decode()
        self.client.credentials(HTTP_AUTHORIZATION='Basic ' + credentials)
        response = self.client.post(url, data=self.data_point, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual('SUCCESS', response.data)
        self.assertEqual(1, models.RFC6349TestDevice.objects.all().count())

    def test_register_using_agent_account(self):
        """ Registering a device hash should fail if a non-staff account is used"""
        self.assertEqual(0, models.RFC6349TestDevice.objects.all().count())

        url = '/api/register'
        credentials = base64.b64encode(('%s:%s' % (self.username, self.password)).encode()).decode()
        self.client.credentials(HTTP_AUTHORIZATION='Basic ' + credentials)
        response = self.client.post(url, data=self.data_point, format='json')
        self.assertEqual(404, response.status_code)
        self.assertEqual('ERROR: User does not exist', response.data)
        self.assertEqual(0, models.RFC6349TestDevice.objects.all().count())

    def test_register_using_bad_hash(self):
        """ Registering a bad device hash should fail """
        self.assertEqual(0, models.RFC6349TestDevice.objects.all().count())

        url = '/api/register'
        self.data_point = {
            "hash": 'bad hash'
        }
        credentials = base64.b64encode(('%s:%s' % (self.staff_username, self.password)).encode()).decode()
        self.client.credentials(HTTP_AUTHORIZATION='Basic ' + credentials)
        response = self.client.post(url, data=self.data_point, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual('ERROR: Invalid hash', response.data)
        self.assertEqual(0, models.RFC6349TestDevice.objects.all().count())

    def test_register_existing_hash(self):
        """ Registering an existing device hash should fail """
        self.assertEqual(0, models.RFC6349TestDevice.objects.all().count())
        self.test_register_normal()
        self.assertEqual(1, models.RFC6349TestDevice.objects.all().count())

        url = '/api/register'
        credentials = base64.b64encode(('%s:%s' % (self.staff_username, self.password)).encode()).decode()
        self.client.credentials(HTTP_AUTHORIZATION='Basic ' + credentials)
        response = self.client.post(url, data=self.data_point, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual('ERROR: Hash already exists', response.data)