from django.urls import path
from django.urls import include
from netmesh_api.views import api1
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'servers', api1.ServerViewSet)

urlpatterns = []

urlpatterns += [
    path('', include(router.urls)),
]

urlpatterns += [
    path('submit', api1.SubmitData.as_view()),
    path('register', api1.Register.as_view()),
    path('submit/traceroute', api1.SubmitTraceroute.as_view()),
]