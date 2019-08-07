from crispy_forms.helper import FormHelper
from django import forms
from django.contrib import messages as alerts
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils.translation import ugettext as _

from netmesh_api.models import AgentProfile


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-8'
        self.helper.form_tag = False

    class Meta:
        model = User
        fields = ['username', 'password']


class AgentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AgentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-8'
        self.helper.form_tag = False

    class Meta:
        model = AgentProfile
        fields = ['ntc_region', 'device']


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


@login_required
def agent_create(request, template_name='agents/form.html'):
    user_form = UserForm(request.POST or None)
    agent_form = AgentForm(request.POST or None)

    if user_form.is_valid() and agent_form.is_valid():
        user_instance = user_form.save(commit=False)
        user_instance.password = make_password(user_form.cleaned_data['password'])
        user_instance = user_form.save()
        agent_instance = agent_form.save(commit=False)
        agent_instance.user = user_instance
        agent_instance.save()
        alerts.success(
            request,
            _("You've successfully created agent '%s.'") % agent_instance
        )
        return agent_list(request)

    my_form = {
        'user_form': user_form,
        'agent_form': agent_form
    }
    return render(request, template_name, my_form)


@login_required
def agent_update(request, pk, template_name='agents/form.html'):
    agent = get_object_or_404(AgentProfile, pk=pk)
    user = agent.user
    user.password = ""  # so that we wont see hash of the old password
    user_form = UserForm(request.POST or None, instance=user)
    agent_form = AgentForm(request.POST or None, instance=agent)

    if user_form.is_valid() and agent_form.is_valid():
        user_instance = user_form.save(commit=False)
        user_instance.password = make_password(user_form.cleaned_data['password'])
        user_instance = user_form.save()
        agent_instance = agent_form.save(commit=False)
        agent_instance.user = user_instance
        agent_instance.save()
        alerts.success(
            request,
            _("You've successfully updated agent '%s.'") % agent_instance
        )
        return agent_list(request)

    my_form = {
        'user_form': user_form,
        'agent_form': agent_form
    }
    return render(request, template_name, my_form)
