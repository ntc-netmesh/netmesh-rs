from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages as alerts
from django.utils.translation import ugettext as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

from netmesh_web.forms import SearchForm

from netmesh_api.models import Server


@login_required
def server_list(request, template_name='servers/list.html'):
    servers_list = Server.objects.all().order_by('-pk')
    paginator = Paginator(servers_list, 15)
    page = request.GET.get('page')
    servers = paginator.get_page(page)
    context = {
        'servers': servers
    }
    return render(request, template_name, context=context)