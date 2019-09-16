from crispy_forms.helper import FormHelper
from django import forms
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from netmesh_api.models import Server
from netmesh_api.models import Speedtest
from netmesh_api.utils import get_client_ip


def do_speedtest(request, template_name='speedtest/main.html'):
    server_list = Server.objects.filter(type='web-based').values_list('nickname', 'hostname', named=True).order_by(
        'nickname')
    client_ip = get_client_ip(request)
    context = {
        'server_list': server_list,
        'client_ip': client_ip
    }
    return render(request, template_name, context=context)


def speedtest_list(request, template_name='speedtest/list.html'):
    test_lst = Speedtest.objects.all().order_by('-date')
    paginator = Paginator(test_lst, 15)
    page = request.GET.get('page')
    speedtests = paginator.get_page(page)
    context = {
        'speedtests': speedtests
    }
    return render(request, template_name, context=context)