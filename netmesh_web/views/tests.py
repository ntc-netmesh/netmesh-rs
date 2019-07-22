from django.shortcuts import render
from netmesh_api.models import Test
from netmesh_api.models import DataPoint
from django.shortcuts import get_object_or_404


def test_detail(request, id, template_name='tests/detail.html'):
    test = get_object_or_404(Test, id=id)
    measurements = DataPoint.objects.filter(test_id=id)

    context = {
        'test': test,
        'measurements': measurements
    }
    return render(request, template_name, context)


def test_list(request, template_name='tests/list.html'):
    tests = Test.objects.all().order_by('-date_created')
    data = DataPoint.objects.all().order_by('-pk')
    context = {
        'tests': tests,
        'data': data
    }
    return render(request, template_name, context=context)