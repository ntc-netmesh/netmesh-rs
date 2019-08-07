from rest_framework import serializers
from netmesh_api.models import Server


class ServerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Server
        fields = ['uuid', 'ip_address']
