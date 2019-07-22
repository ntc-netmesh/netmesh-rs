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
    server_list = Server.objects.all()
    paginator = Paginator(server_list, 10)  # Show 25 contacts per page

    page = request.GET.get('page')
    servers = paginator.get_page(page)
    data = {
        'servers': servers,
        'server_list': server_list
    }
    return render(request, template_name, data)