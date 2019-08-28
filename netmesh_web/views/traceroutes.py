from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from netmesh_api.models import Hop
from netmesh_api.models import Traceroute


def traceroute_detail(request, id, template_name='traceroute/detail.html'):
    traceroute = get_object_or_404(Traceroute, id=id)
    hops = Hop.objects.filter(traceroute=id)

    context = {
        'traceroute': traceroute,
        'hops': hops
    }
    return render(request, template_name, context)


def traceroute_list(request, template_name='traceroute/list.html'):
    traceroutes = Traceroute.objects.all().order_by('-date')
    paginator = Paginator(traceroutes, 15)
    page = request.GET.get('page')
    traceroutes = paginator.get_page(page)
    context = {
        'traceroutes': traceroutes
    }
    return render(request, template_name, context=context)
