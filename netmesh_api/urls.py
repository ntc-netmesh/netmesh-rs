from django.urls import path
from netmesh_api.views import api1

urlpatterns = []

urlpatterns += [
    path('submit', api1.SubmitData.as_view()),
    path('register', api1.Register.as_view()),
]