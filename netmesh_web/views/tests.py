import djqscsv
from django.contrib import messages as alerts
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.template import loader
from django.utils.translation import ugettext as _

from netmesh_api.models import DataPoint
from netmesh_api.models import Test
from netmesh_web.forms import SearchForm


def test_detail(request, id, template_name='tests/detail.html'):
    test = get_object_or_404(Test, id=id)
    measurements = DataPoint.objects.filter(test_id=id)

    context = {
        'test': test,
        'measurements': measurements
    }
    return render(request, template_name, context)


def test_list(request, template_name='tests/list.html'):
    context = {}
    if 'search' in request.GET:
        test_lst = Test.objects.all().order_by('-date_created')
        for term in request.GET['search'].split():
            test_lst = test_lst.filter(Q(test_type__icontains=term) |
                                       Q(mode__icontains=term) |
                                       Q(ip_address__ip_address__icontains=term) |
                                       Q(ip_address__isp__icontains=term) |
                                       Q(agent__user__username__icontains=term)
                                       )
        context['search'] = True
        alerts.info(request,
                    _("You've searched for: '%s'") % request.GET['search'])
    else:
        test_lst = Test.objects.all().order_by('-date_created')

    paginator = Paginator(test_lst, 15)
    page = request.GET.get('page')

    is_paginated = False
    if paginator.num_pages > 1:
        is_paginated = True

    try:
        tests = paginator.get_page(page)
    except PageNotAnInteger:
        tests = paginator.get_page(1)
    except EmptyPage:
        tests = paginator.get_page(paginator.num_pages)

    form = SearchForm(form_action='tests')
    context = {
        'tests': tests,
        'form': form,
        'is_paginated': is_paginated
    }
    return render(request, template_name, context=context)


def datapoint_detail(request, id, template_name='tests/datapoint_detail.html'):
    datapoint = DataPoint.objects.get(id=id)

    context = {
        'datapoint': datapoint
    }
    return render(request, template_name, context)


def get_csv(request):
    qs = DataPoint.objects.values('date_tested',
                                  'test_id',
                                  'test_id__agent__user__username',
                                  'test_id__ip_address__ip_address',
                                  'test_id__ip_address__isp',
                                  'test_id__test_type',
                                  'test_id__network_connection',
                                  # 'test_id__pcap',
                                  # 'test_id__lat',
                                  # 'test_id__long',
                                  'test_id__mode',
                                  'test_id__device__hash',
                                  'server__uuid',
                                  'server__nickname',
                                  'server__ip_address',
                                  'direction',
                                  'path_mtu',
                                  'baseline_rtt',
                                  'bottleneck_bw',
                                  'bdp',
                                  'min_rwnd',
                                  'ave_tcp_tput',
                                  'ideal_tcp_tput',
                                  'actual_transfer_time',
                                  'ideal_transfer_time',
                                  'tcp_ttr',
                                  'trans_bytes',
                                  'retrans_bytes',
                                  'tcp_eff',
                                  'ave_rtt',
                                  'buffer_delay'
                                  )
    return djqscsv.render_to_csv_response(qs,
                                          filename='ntc-netmesh-rfc6349',
                                          append_datestamp=True,
                                          streaming=True)
