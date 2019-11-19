from django.urls import path
from netmesh_web.views import index
from netmesh_web.views import agents
from netmesh_web.views import servers
from netmesh_web.views import tests
from netmesh_web.views import users
from netmesh_web.views import traceroutes
from netmesh_web.views import speedtest
from netmesh_web.views import staff


urlpatterns = []

""" Main results page """
urlpatterns += [
    path('', index.map, name='index'),
    path('map/', index.map, name='map'),
    path('about/', index.about, name='about'),
    path('contact/', index.contact, name='contact'),
]

""" Users """
urlpatterns += [
    path('tz/', users.set_timezone, name='set_timezone'),
]

""" Agents """
urlpatterns += [
    path('agents/', agents.agent_list, name='agents'),
    path('agents/create/', agents.agent_create, name='agent_create'),
    path('agents/update/<pk>', agents.agent_update, name='agent_update'),
]

""" Servers """
urlpatterns += [
    path('servers/', servers.server_list, name='servers'),
    path('servers/create', servers.server_create, name='server_create'),
    path('servers/update/<uuid>', servers.server_update, name='server_update'),
]

""" Tests """
urlpatterns += [
    path('tests/', tests.test_list, name='tests'),
    path('tests/detail/<id>', tests.test_detail, name='test_detail'),
    path('datapoint/detail/<id>', tests.datapoint_detail, name='datapoint_detail'),
    path('tests/csv', tests.get_csv, name='tests_csv'),
]

""" Traceroutes """
urlpatterns += [
    path('traceroutes/', traceroutes.traceroute_list, name='traceroutes'),
    path('traceroutes/detail/<id>', traceroutes.traceroute_detail, name='traceroute_detail'),
]

""" Speedtests """
urlpatterns += [
    path('speedtest/', speedtest.do_speedtest, name='speedtest'),
    path('speedtest/list', speedtest.speedtest_list, name='speedtest_list'),
    path('speedtest/csv', speedtest.get_csv, name='speedtest_csv'),
]

""" Staff """
urlpatterns += [
    path('staff/', staff.staff_list, name='staff'),
    path('staff/create/', staff.staff_create, name='staff_create'),
    path('staff/update/<pk>', staff.staff_update, name='staff_update'),
]
