from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages as alerts
from django.utils.translation import ugettext as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

from netmesh_web.forms import SearchForm

from netmesh_api.models import AgentProfile



@login_required
def agent_list(request, template_name='agents/list.html'):
    data = {}
    if 'search' in request.GET:
        agents = AgentProfile.objects.filter(
            Q(nickname__icontains=request.GET['search'])
            | Q(user_username__icontains=request.GET['search'])
            | Q(device__icontains=request.GET[
                'search'])).order_by('-date_created')
        data['search'] = True
        alerts.info(
            request, _("You've searched for: '%s'") % request.GET['search'])
    else:
        agents = AgentProfile.objects.all().order_by('-date_created')
    #
    # paginator = Paginator(agents, 15)
    #
    # page = request.GET.get('page')
    #
    # is_paginated = False
    # if paginator.num_pages > 1:
    #     is_paginated = True
    #
    # try:
    #     agents = paginator.page(page)
    # except PageNotAnInteger:
    #     agents = paginator.page(1)
    # except EmptyPage:
    #     agents = paginator.page(paginator.num_pages)
    #
    # form = SearchForm(form_action='agents')
    # data = {
    #     "agents": agents,
    #     "is_paginated": is_paginated,
    #     "form": form
    # }
    data = {
        "agents": AgentProfile.objects.all()
    }

    return render(request, template_name, data)