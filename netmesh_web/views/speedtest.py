import djqscsv
from crispy_forms.helper import FormHelper
from django import forms
from django.contrib import messages as alerts
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt

from netmesh_api.models import Server
from netmesh_api.models import Speedtest
from netmesh_api.utils import get_client_ip
from netmesh_web.forms import SearchForm


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
    context = {}
    if 'search' in request.GET:
        test_lst = Speedtest.objects.all().order_by('-date')
        for term in request.GET['search'].split():
            test_lst = test_lst.filter(Q(server__nickname__icontains=term) |
                                       Q(ip_address__ip_address__icontains=term) |
                                       Q(ip_address__isp__icontains=term)
                                       )
        context['search'] = True
        alerts.info(request,
                    _("You've searched for: '%s'") % request.GET['search'])
    else:
        test_lst = Speedtest.objects.all().order_by('-date')

    paginator = Paginator(test_lst, 15)
    page = request.GET.get('page')

    is_paginated = False
    if paginator.num_pages > 1:
        is_paginated = True

    try:
        speedtests = paginator.get_page(page)
    except PageNotAnInteger:
        speedtests = paginator.get_page(1)
    except EmptyPage:
        speedtests = paginator.get_page(paginator.num_pages)

    form = SearchForm(form_action='speedtest_list')
    context = {
        'speedtests': speedtests,
        'form': form,
        'is_paginated': is_paginated
    }
    return render(request, template_name, context=context)

def get_csv(request):
    qs = Speedtest.objects.values('date',
                                  'test_id',
                                  'sid',
                                  'ip_address__ip_address',
                                  'ip_address__isp',
                                  'server__uuid',
                                  'server__nickname',
                                  'server__ip_address',
                                  'rtt_ave',
                                  'rtt_min',
                                  'rtt_max',
                                  'upload_speed',
                                  'download_speed'
                                  )
    return djqscsv.render_to_csv_response(qs,
                                          filename='ntc-netmesh-web-based',
                                          append_datestamp=True,
                                          streaming=True)
