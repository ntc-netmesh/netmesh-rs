from django.urls import path
from netmesh_web.views import index
from netmesh_web.views import agents
from netmesh_web.views import servers


urlpatterns = []

""" Main results page """
urlpatterns += [
    path('', index.home, name='index'),
]

""" Agents """
urlpatterns += [
    path('agents/', agents.agent_list, name='agents'),
    path('servers/', servers.server_list, name='servers'),
]