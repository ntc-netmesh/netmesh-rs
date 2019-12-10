"""
    Forms for manual input of Network Master Pro data
"""

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML
from crispy_forms.layout import Submit
from django import forms
from django.contrib import messages as alerts
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _

from netmesh_api.models import NMProDataPoint
from netmesh_web.views import index


class NMProFormDatapoint(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NMProFormDatapoint, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.label_class = 'col-sm-3'
        self.helper.field_class = 'col-sm-7'
        self.helper.layout.append(Submit('save', 'Save', css_class='btn btn-sm btn-primary'))
        self.helper.layout.append(HTML(
            '<a href="{}" class="btn btn-sm btn-outline-secondary" role="button">{}</a>'.format(
                reverse_lazy('index', kwargs={}),
                'Cancel')
        ))

    class Meta:
        model = NMProDataPoint
        exclude = ['date_created']


@login_required
def nmpro_data_create(request, template_name='nmpro/form.html'):
    datapoint_form = NMProFormDatapoint(request.POST or None)

    if datapoint_form.is_valid():
        datapoint_form.save()
        return index.map(request)

    my_form = {
        'datapoint_form': datapoint_form
    }
    return render(request, template_name, my_form)
