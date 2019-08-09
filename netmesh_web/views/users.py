import pytz
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.context_processors import csrf
from django.template.loader import get_template
from django.urls import reverse

from netmesh_api.models import AgentProfile


def loginview(request):
    """Show the login page.

    If 'next' is a URL parameter, add its value to the context.  (We're
    mimicking the standard behavior of the django login auth view.)
    """
    context = {
        'next': request.GET.get('next', ''),
    }
    context.update(csrf(request))
    template = get_template("registration/login.html")
    html = template.render(context, request)
    return HttpResponse(html)


def auth_and_login(request):
    """Handles POSTed credentials for login."""
    user = authenticate(username=request.POST['username'],
                        password=request.POST['password'])
    if user is not None:
        if user.is_active:
            # check if user is an agent
            try:
                agent_profile = AgentProfile.objects.get(user=user)
            except AgentProfile.DoesNotExist:
                agent_profile = None
            if agent_profile:
                text = "Agent accounts are not allowed. Please contact admin."
                print(text)
                messages.error(request, text)
                return redirect(reverse('login'))
            # else, this is a regular user
            else:
                login(request, user)
                next_url = reverse('map')
                if 'next' in request.POST and request.POST['next']:
                    next_url = request.POST['next']
                    return redirect(next_url)
                else:
                    return redirect(next_url)
        else:
            # Notification, if blocked user is trying to log in
            text = "This user is blocked. Please contact admin."
            messages.error(request, text)
            return redirect(reverse('login'))
    else:
        text = "Sorry, that username / password combination is not valid."
        messages.error(request, text)
        return redirect(reverse('login'))



def set_timezone(request):
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')
    else:
        return render(request, 'users/tz.html', {'timezones': pytz.common_timezones})