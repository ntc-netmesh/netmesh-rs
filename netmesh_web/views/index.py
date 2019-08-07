from django.shortcuts import render

from netmesh_api.models import DataPoint


def home(request):
    context = {
    }
    return render(request, 'index.html', context=context)


def map(request):
    context = {
        "datapoints": DataPoint.objects.all().order_by('test_id')
    }
    return render(request, 'map.html', context=context)

