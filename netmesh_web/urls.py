from django.urls import path
from netmesh_web.views import index
from netmesh_web.views import agents


urlpatterns = []

""" Main results page """
urlpatterns += [
    path('', index.home, name='index'),
]

""" Agents """
urlpatterns += [
    path('agents/', agents.agent_list, name='agents')
]