from django.shortcuts import render
from netmesh_api.models import Test


def index(request):
    tests = Test.objects.all()
    context = {
        'tests': tests
    }
    return render(request, 'index.html', context=context)

