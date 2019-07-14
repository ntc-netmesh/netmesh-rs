import uuid
import pytz

import django.utils.timezone
import itsdangerous
import pytz
# import stripe
from django.conf import settings
from django.contrib.auth.models import Group, User
# from django.contrib.gis.db import models as geomodels

from django.contrib.auth.models import Group, User
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.db import models
from netmesh import choices
from random import randint


class UserProfile(models.Model):
    """ UserProfiles extend the default Django User models
        specifically to represent users who will be able to log-in
        on the Netmesh results server website
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    timezone_choices = [(v, v) for v in pytz.common_timezones]
    timezone = models.CharField(max_length=50, default='UTC',
                                choices=timezone_choices)
    role = models.CharField(max_length=20, default='Cloud Admin')
    # Added for Password Expiry
    last_pwd_update = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'netmesh_api_userprofile'
        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfiles'
        ordering = ['-id']

    def __str__(self):
        return "%s's profile" % self.user

    def display_name(self):
        if self.user.get_short_name():
            return self.user.get_short_name()
        else:
            return self.user.username


class AgentProfile(models.Model):
    """ Extension of the User model specificall for the test clients (aka  Agents)"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    nickname = models.CharField(max_length=1024, null=True, blank=True)
    ntc_region = models.CharField(max_length=20, choices=choices.ntc_region_choices, default='unknown')
    device = models.CharField(max_length=20, choices=choices.device_choices, default='unknown')
    registration_status = models.CharField(
        max_length=20, choices=choices.registration_choices, default='unregistered')
    certificate = models.TextField(null=True)
    secret = models.TextField(null=True)


    @property
    def latitude(self):
        return self.location.y

    @property
    def longitude(self):
        return self.location.x

    def generate_jwt(self, data_dict):
        """Generate a JSON web token for this Agent.

        IMPORTANT: This is subject to replay attacks if there's not a nonce in
        the JWT. It's the callers responsibility to include this in the data
        dict if replay attacks are a concern (a random, unique msgid would
        suffice).
        """
        serializer = itsdangerous.JSONWebSignatureSerializer(self.secret)
        return serializer.dumps(data_dict)


class Server(models.Model):
    """ Model for a NetMesh test server
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    nickname = models.CharField(max_length=200, null=True)
    ip_address = models.GenericIPAddressField()  # assumes that server has a fixed IP address
    type = models.CharField(max_length=20, choices=choices.server_choices, default='unknown')
    gps = models.CharField(max_length=100, null=True)
    # gps = geomodels.GeometryField(geography=True, default='POINT(16.647322, 121.071959)')
    city = models.CharField(max_length=200, null=True)
    province = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, default='Philippines')


class IpAddress(models.Model):
    ip_address = models.GenericIPAddressField()


class Test(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent = models.ForeignKey(AgentProfile, null=False, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(null=False, protocol='IPv4')  # ip address of agent when test was conducted
    test_type = models.CharField(null=False, max_length=10, choices=choices.test_type_choices)
    date_created = models.DateTimeField(auto_now_add=True)
    network_connection = models.CharField(max_length=10, choices=choices.network_choices, default='unknown')
    pcap = models.CharField(max_length=100, null=True)
    gps = models.CharField(max_length=100, null=True)
    # gps = geomodels.GeometryField(geography=True, default='POINT(16.647322, 121.071959)')


class DataPoint(models.Model):
    """Model for a data point which is acquired by the test client against a test server"""
    date_tested = models.DateTimeField()
    test_id = models.ForeignKey(Test, null=False, on_delete=models.CASCADE)
    server = models.ForeignKey(Server, null=False, on_delete=models.CASCADE)
    rtt = models.BigIntegerField(null=True)
    upload_speed = models.BigIntegerField(null=True)
    download_speed = models.BigIntegerField(null=True)
