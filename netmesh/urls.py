"""netmesh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from netmesh_web.views import users

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('api/', include('netmesh_api.urls')),
    path('web/', include('netmesh_web.urls')),
    path('accounts/login/', users.loginview, name='login'),
    path('accounts/auth/', users.auth_and_login, name='auth-and-login'),
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += [
    path('', RedirectView.as_view(url='/web/', permanent=True)),
    path('accounts', RedirectView.as_view(url='/accounts/login', permanent=True))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)