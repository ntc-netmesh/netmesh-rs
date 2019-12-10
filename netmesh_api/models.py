import uuid
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone as timezone

from netmesh_api import choices


class UserProfile(models.Model):
    """ UserProfiles extend the default Django User models
        specifically to represent users who will be able to log-in
        on the Netmesh results server website
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    timezone = models.CharField(max_length=50, default='Asia/Manila',
                                choices=choices.timezone_choices)
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
    """
        Extension of the User model specifically for the test clients (aka  Agents)
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    ntc_region = models.CharField(max_length=20, choices=choices.ntc_region_choices, default='unknown')
    device = models.CharField(max_length=20, choices=choices.device_choices, default='computer')
    registration_status = models.CharField(max_length=20, choices=choices.registration_choices, default='unregistered')

    def __str__(self):
        return "%s" % self.user

    def display_name(self):
        if self.user.get_short_name():
            return self.user.get_short_name()
        else:
            return self.user.username


class IPaddress(models.Model):
    """
        Model for IP addresses containing its geolocation & ISP data
    """
    date = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=False)
    country = models.CharField(max_length=50)
    country_code = models.CharField(max_length=10)
    region = models.CharField(max_length=50)
    region_name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip = models.CharField(max_length=10)
    lat = models.FloatField(default=0, validators=[MaxValueValidator(90.0), MinValueValidator(-90.0)])
    long = models.FloatField(default=0, validators=[MaxValueValidator(180.0), MinValueValidator(-180.0)])
    timezone = models.CharField(max_length=50, default='Asia/Manila',
                                choices=choices.timezone_choices)
    isp = models.CharField(max_length=100)
    org = models.CharField(max_length=100)
    as_num = models.CharField(max_length=100)
    as_name = models.CharField(max_length=100)
    reverse = models.CharField(max_length=200)
    mobile = models.BooleanField(default=False)
    proxy = models.BooleanField(default=False)


class Server(models.Model):
    """
        Model for a NetMesh test server
        The same model is used for both RFC-6349 test servers and Web-based speedtest servers
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    nickname = models.CharField(max_length=200, null=True)
    ip_address = models.GenericIPAddressField()  # assumes that server has a fixed IP address
    type = models.CharField(max_length=20, choices=choices.server_choices, default='unknown')
    test_method = models.CharField(null=False, max_length=50, choices=choices.test_type_choices, default='0')
    lat = models.FloatField(default=16.647322, validators=[MaxValueValidator(90.0), MinValueValidator(-90.0)])
    long = models.FloatField(default=121.071959, validators=[MaxValueValidator(180.0), MinValueValidator(-180.0)])
    city = models.CharField(max_length=200, null=True)
    province = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, default='Philippines')
    sponsor = models.CharField(max_length=200, default='SponsorName')  # organization that hosts this server
    hostname = models.URLField(max_length=500, default="http://dummyhostname.com")

    def __str__(self):
        return "Server %s (%s)" % (self.nickname, self.uuid)


class RFC6349TestDevice(models.Model):
    """
        Model for the hardware device used by the RFC-6349 test agents
    """
    date_created = models.DateTimeField(auto_now_add=True)
    hash = models.CharField(max_length=64, unique=True, null=False)
    created_by = models.ForeignKey(UserProfile, null=False, on_delete=models.CASCADE)
    device_id = models.UUIDField(default=uuid.uuid4, unique=True)

    class Meta:
        verbose_name = 'RFC6349 Test Device'
        verbose_name_plural = 'RFC6349 Test Devices'
        ordering = ['-id']


class Test(models.Model):
    """
        Model to represent results from an RFC-6349 Test
        Each test can contain multiple datapoints (i.e. forward, reverse).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent = models.ForeignKey(AgentProfile, null=False, on_delete=models.CASCADE)
    # ip_address = models.GenericIPAddressField(null=False, protocol='IPv4')  # IP addr of agent when test was conducted
    ip_address = models.ForeignKey(IPaddress, on_delete=models.CASCADE)
    test_type = models.CharField(null=False, max_length=50, choices=choices.test_type_choices)
    date_created = models.DateTimeField(auto_now_add=True)
    network_connection = models.CharField(max_length=20, null=False, default='unknown')
    pcap = models.CharField(max_length=100, null=True)
    lat = models.FloatField(default=16.647322, validators=[MaxValueValidator(90.0), MinValueValidator(-90.0)])
    long = models.FloatField(default=121.071959, validators=[MaxValueValidator(180.0), MinValueValidator(-180.0)])
    mode = models.CharField(null=False, max_length=50, choices=choices.test_mode_choices, default='unknown')
    device = models.ForeignKey(RFC6349TestDevice, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return "Test %s" % self.id


class DataPoint(models.Model):
    """
        Model for an RFC-6349 test datapoint
    """
    date_tested = models.DateTimeField(blank=True, default=timezone.now)
    test_id = models.ForeignKey(Test, null=False, on_delete=models.CASCADE)
    direction = models.CharField(null=False, max_length=10, choices=choices.direction_choices, default='unknown')
    server = models.ForeignKey(Server, null=False, on_delete=models.CASCADE)
    path_mtu = models.IntegerField(null=True)  # Path Max Transmit Unit, in bytes
    baseline_rtt = models.FloatField(null=True)  # Baseline Round Trip Time, in ms
    bottleneck_bw = models.FloatField(null=True)  # Bottleneck Bandwidth, in Mbps
    bdp = models.FloatField(null=True)  # Bandwidth Delay Product, in bits
    min_rwnd = models.FloatField(null=True)  # Minimum Receive Window Size, in Kbytes
    ave_tcp_tput = models.FloatField(null=True)  # Average TCP Throughput, in Mbps
    ideal_tcp_tput = models.FloatField(null=True)  # Ideal TCP throughput, in Mbps
    actual_transfer_time = models.FloatField(null=True)  # Actual Transfer Time, in secs
    ideal_transfer_time = models.FloatField(null=True)  # Ideal Transfer Time, in secs
    tcp_ttr = models.FloatField(null=True)  # TCP transfer Time Ratio, unitless
    trans_bytes = models.FloatField(null=True)  # Transmitted Bytes, in bytes
    retrans_bytes = models.FloatField(null=True)  # Retransmitted Bytes, in bytes
    tcp_eff = models.FloatField(null=True)  # TCP Efficiency, in %
    ave_rtt = models.FloatField(null=True)  # Average Round Trip Time, in ms
    buffer_delay = models.FloatField(null=True)  # Buffer Delay, in %


class Traceroute(models.Model):
    """
        Model for traceroute information
        Each traceroute can have one or more associated Hops
    """
    date = models.DateTimeField(default=timezone.now)
    origin_ip = models.GenericIPAddressField(null=False)
    dest_ip = models.GenericIPAddressField(null=False)
    dest_name = models.CharField(max_length=200, null=False)


class Hop(models.Model):
    """
        Model for a traceroute Hop
    """
    traceroute = models.ForeignKey(Traceroute, null=False, on_delete=models.CASCADE)
    hop_index = models.IntegerField(null=False)
    time1 = models.FloatField(null=True)
    time2 = models.FloatField(null=True)
    time3 = models.FloatField(null=True)
    host_name = models.CharField(max_length=200)  # domain name or fallback to IP address if no domain name
    host_ip = models.GenericIPAddressField(null=True)


class Speedtest(models.Model):
    """
        Model to represent results from a web-based speedtest.
        Note that the web-based speedtest is simpler compared to the RFC-6349 result representation
    """
    date = models.DateTimeField(default=timezone.now)
    test_id = models.UUIDField(null=False, editable=False, unique=True)
    sid = models.CharField(max_length=32, null=False, editable=False)
    ip_address = models.ForeignKey(IPaddress, on_delete=models.CASCADE)
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    rtt_ave = models.FloatField(null=False)
    rtt_min = models.FloatField(null=False)
    rtt_max = models.FloatField(null=False)
    upload_speed = models.FloatField(null=False)
    download_speed = models.FloatField(null=False)


class NMProDataPoint(models.Model):
    """
        Model for a manually entered NetMaster Pro measurement
    """
    date_created = models.DateTimeField(blank=True, default=timezone.now)
    ip_address = models.GenericIPAddressField(null=False, verbose_name='Client IP address')
    server = models.GenericIPAddressField(null=False, verbose_name='Server IP address')
    lat = models.FloatField(default=16.647322, validators=[MaxValueValidator(90.0), MinValueValidator(-90.0)],
                            verbose_name='Latitude')
    long = models.FloatField(default=121.071959, validators=[MaxValueValidator(180.0), MinValueValidator(-180.0)],
                             verbose_name='Longitude')
    mode = models.CharField(null=False, max_length=10, default='unknown',
                            choices=[('auto', 'Auto'), ('expert', 'Expert'), ('unknown', 'Unknown')])

    # Test conditions section

    direction = models.CharField(null=False, max_length=10, choices=choices.direction_choices, default='unknown')
    min_rwnd = models.FloatField(null=True, verbose_name='Minimum Receive Window Size', help_text='in bytes')
    connections = models.IntegerField(null=True, verbose_name='Connections', help_text='enter number of connections')
    bdp = models.FloatField(null=True, verbose_name='Bandwidth Delay Product', help_text='in bytes')
    path_mtu = models.IntegerField(null=True, verbose_name='Path MTU', help_text='in bytes')
    baseline_rtt = models.FloatField(null=True, verbose_name='Baseline RTT', help_text='in ms')
    cir = models.FloatField(null=True, verbose_name='CIR', help_text='in Mbps')
    bottleneck_bw = models.FloatField(null=True, verbose_name='Bottleneck Bandwidth', help_text='in Mbps')

    # TCP throughput section
    ave_tcp_tput = models.FloatField(null=True, verbose_name='Average TCP Throughput', help_text='in Mbps')
    ideal_tcp_tput = models.FloatField(null=True, verbose_name='Ideal TCP throughput', help_text='in Mbps')
    threshold = models.FloatField(null=True, verbose_name='Threshold', help_text='in %')

    # Transfer Time section
    actual_transfer_time = models.FloatField(null=True, verbose_name='Actual Transfer Time', help_text='in secs')
    ideal_transfer_time = models.FloatField(null=True, verbose_name='Ideal Transfer Time', help_text='in secs')
    tcp_ttr = models.FloatField(null=True, verbose_name='TCP transfer Time Ratio', help_text='unitless')

    # Data Transfer section
    trans_bytes = models.FloatField(null=True, verbose_name='Transmitted Bytes', help_text='in bytes')
    retrans_bytes = models.FloatField(null=True, verbose_name='Retransmitted Bytes', help_text='in bytes')
    tcp_eff = models.FloatField(null=True, verbose_name='TCP Efficiency', help_text='in %')

    # RTT Section
    min_rtt = models.FloatField(null=True, verbose_name='Minimum Round Trip Time', help_text='in ms')
    max_rtt = models.FloatField(null=True, verbose_name='Maximum Trip Time', help_text='in ms')
    ave_rtt = models.FloatField(null=True, verbose_name='Average Round Trip Time', help_text='in ms')
    buffer_delay = models.FloatField(null=True, verbose_name='Buffer Delay', help_text='in %')
