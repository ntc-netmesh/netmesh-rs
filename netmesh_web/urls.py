from django.urls import path
from netmesh_web.views import index
from netmesh_web.views import agents
from netmesh_web.views import servers
from netmesh_web.views import tests
from netmesh_web.views import users


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
]