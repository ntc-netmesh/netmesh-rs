from django.shortcuts import render
from netmesh_api.models import DataPoint
from netmesh_api.models import Test


def home(request):
    context = {
    }
    return render(request, 'index.html', context=context)


def map(request):
    context = {
        "datapoints": DataPoint.objects.all(),
        "tests": Test.objects.all()
    }
    return render(request, 'map.html', context=context)

