from django.shortcuts import render

from netmesh_api.models import DataPoint
from netmesh_api.models import Speedtest


def home(request):
    return render(request, 'index.html', {})


def about(request):
    return render(request, 'about.html', {})


def contact(request):
    return render(request, 'contact.html', {})


def map(request):
    context = {
        "datapoints": DataPoint.objects.all().order_by('test_id'),
        "speedtests": Speedtest.objects.all().order_by('pk')
    }
    return render(request, 'map.html', context=context)

