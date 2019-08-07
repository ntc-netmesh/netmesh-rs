from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from netmesh_api.models import DataPoint
from netmesh_api.models import Test


def test_detail(request, id, template_name='tests/detail.html'):
    test = get_object_or_404(Test, id=id)
    measurements = DataPoint.objects.filter(test_id=id)

    context = {
        'test': test,
        'measurements': measurements
    }
    return render(request, template_name, context)


def test_list(request, template_name='tests/list.html'):
    test_lst = Test.objects.all().order_by('-date_created')
    paginator = Paginator(test_lst, 15)
    page = request.GET.get('page')
    tests = paginator.get_page(page)
    context = {
        'tests': tests
    }
    return render(request, template_name, context=context)


def datapoint_detail(request, id, template_name='tests/datapoint_detail.html'):
    datapoint = DataPoint.objects.get(id=id)

    context = {
        'datapoint': datapoint
    }
    return render(request, template_name, context)