from django.shortcuts import render
from netmesh_api.models import Test
from netmesh_api.models import DataPoint


def home(request):
    tests = Test.objects.all()
    data = DataPoint.objects.all()
    context = {
        'tests': tests,
        'data': data
    }
    return render(request, 'index.html', context=context)

