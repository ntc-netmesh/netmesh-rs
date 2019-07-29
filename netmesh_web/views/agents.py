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
    agent_list = AgentProfile.objects.all().order_by('-pk')
    paginator = Paginator(agent_list, 10)  # Show 25 contacts per page
    page = request.GET.get('page')
    agents = paginator.get_page(page)
    data = {
        'agents': agents,
    }
    return render(request, template_name, data)