from django.urls import path
from netmesh_web.views import index
from netmesh_web.views import dashboard
import django


urlpatterns = []
#
# """ Auth """
# urlpatterns += [
#     path('login/', django.contrib.auth.views.login, {'template_name': 'accounts/login.html'}, name="login"),
#     path('logout/', django.contrib.auth.views.logout, {'template_name': 'accounts/logout.html'}, name="logout"),
# ]


urlpatterns += [
    path('', index.home, name='index'),
    path('ne/', dashboard.home, name='home')
]