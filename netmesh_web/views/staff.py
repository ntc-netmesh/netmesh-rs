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

from netmesh_api.models import UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-8'
        self.helper.form_tag = False

    def is_password(field):
        return isinstance(field.field.widget, forms.PasswordInput)

    def clean(self, *args, **kwargs):
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            raise forms.ValidationError('The passwords do not match!')
        return super(UserForm, self).clean(*args, **kwargs)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password',
                  'first_name', 'last_name', 'email']


class StaffForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-8'
        self.helper.form_tag = False

    class Meta:
        model = UserProfile
        fields = ['role', 'timezone']


@login_required
def staff_list(request, template_name='staff/list.html'):
    staff_list = UserProfile.objects.all().order_by('-pk')
    paginator = Paginator(staff_list, 10)  # Show 25 contacts per page
    page = request.GET.get('page')
    staffs = paginator.get_page(page)
    data = {
        'staffs': staffs,
    }
    return render(request, template_name, data)


@login_required
def staff_create(request, template_name='staff/form.html'):
    user_form = UserForm(request.POST or None)
    staff_form = StaffForm(request.POST or None)

    if user_form.is_valid() and staff_form.is_valid():
        user_instance = user_form.save(commit=False)
        user_instance.password = make_password(user_form.cleaned_data['password'])
        user_instance = user_form.save()
        staff_instance = staff_form.save(commit=False)
        staff_instance.user = user_instance
        staff_instance.save()
        alerts.success(
            request,
            _("You've successfully created staff '%s.'") % staff_instance
        )
        return staff_list(request)

    my_form = {
        'user_form': user_form,
        'staff_form': staff_form
    }
    return render(request, template_name, my_form)


@login_required
def staff_update(request, pk, template_name='staff/update.html'):
    staff = get_object_or_404(UserProfile, pk=pk)
    user_form = UserForm(request.POST or None, instance=staff.user)
    staff_form = StaffForm(request.POST or None, instance=staff)

    if user_form.is_valid() and staff_form.is_valid():
        user_instance = user_form.save(commit=False)
        user_instance.password = make_password(user_form.cleaned_data['password'])
        user_instance = user_form.save()
        staff_instance = staff_form.save(commit=False)
        staff_instance.user = user_instance
        staff_instance.save()
        alerts.success(
            request,
            _("You've successfully updated staff '%s.'") % staff_instance
        )
        return staff_list(request)

    my_form = {
        'user_form': user_form,
        'staff_form': staff_form
    }
    return render(request, template_name, my_form)
