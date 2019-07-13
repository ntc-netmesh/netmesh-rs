from django.urls import path
from netmesh_web.views import views

urlpatterns = [
    path('', views.index, name='index')
]