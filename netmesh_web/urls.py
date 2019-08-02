from django.urls import path
from netmesh_web.views import index
from netmesh_web.views import agents
from netmesh_web.views import servers
from netmesh_web.views import tests


urlpatterns = []

""" Main results page """
urlpatterns += [
    path('', index.home, name='index'),
    path('map/', index.map, name='map'),
]

""" Agents """
urlpatterns += [
    path('agents/', agents.agent_list, name='agents'),
]

""" Servers """
urlpatterns += [
    path('servers/', servers.server_list, name='servers'),
]

""" Tests """
urlpatterns += [
    path('tests/', tests.test_list, name='tests'),
    path('tests/detail/<id>', tests.test_detail, name='test_detail'),
    path('datapoint/detail/<id>', tests.datapoint_detail, name='datapoint_detail'),
]