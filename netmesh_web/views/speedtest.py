from crispy_forms.helper import FormHelper
from django import forms
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from netmesh_api.models import Server
from netmesh_api.utils import get_client_ip


@csrf_exempt
def do_speedtest(request, template_name='speedtest/main.html'):
    server_list = Server.objects.all().order_by('-pk')
    client_ip = get_client_ip(request)
    server_default = Server.objects.get(pk=1)
    context = {
        'server_list': server_list,
        'def_server': server_default,
    }
    return render(request, template_name, context=context)
