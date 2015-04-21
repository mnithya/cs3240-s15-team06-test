from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.core.context_processors import csrf
from django.contrib import auth
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django import forms
from polls.models import Report
from django.contrib.auth.models import UserManager
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group
from django.db.models import Count
from django.forms import ModelForm
from polls.forms import ReportForm
from polls.forms import FolderForm
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from functools import partial
from polls.models import Folder
from django.db.models.expressions import F
from django.db.models import Q
from itertools import chain


# Create your views here.


def home(request):
    c = {}
    c.update(csrf(request))

    return render_to_response('index.html', c)


def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('login.html', c, context_instance=RequestContext(request))


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/accounts/loggedin')
    else:
        return HttpResponseRedirect('/accounts/invalid')


def loggedin(request):
    return render_to_response('loggedin.html',
                              {'full_name': request.user.username,'current_user':request.user.id},context_instance=RequestContext(request))


def invalid_login(request):
    return render_to_response('invalid_login.html')


def logout(request):
    auth.logout(request)
    return render_to_response('logout.html')

@login_required
def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/register_success')
    args = {}
    args.update(csrf(request))

    args['form'] = UserCreationForm()

    return render_to_response('register.html', args)


def register_success(request):
    return render_to_response('register_success.html')

'''
class ReportForm(forms.Form):
    subject = forms.CharField()
    long_text = forms.CharField(widget=forms.Textarea)
    short_text = forms.CharField()
    file = forms.FileField()
    private = forms.BooleanField(required=False)
'''

''''
def new_report(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            rf = ReportForm(request.POST,request.FILES)
            if rf.is_valid():
                #get data from forms
                subject = rf.cleaned_data['subject']
                long_text = rf.cleaned_data['long_text']
                short_text = rf.cleaned_data['short_text']
                file = rf.cleaned_data['file']
                private = rf.cleaned_data['private']
                #writing datas into database
                report = Report()
                report.subject = subject
                report.long_text = long_text
                report.short_text= short_text
                report.file = file
                report.user_id = request.user.id
                report.private = private
                report.save()
                return HttpResponse('upload ok!')
        else:
            rf = ReportForm()
        return render_to_response('report.html', {'rf':rf, 'full_name': request.user.username}, context_instance=RequestContext(request))
    else:
        return render_to_response('index.html', context_instance=RequestContext(request))
'''

@login_required
def user_report(request):
    report_list = Report.objects.filter(user_id=request.user.id)
    folder_list = Folder.objects.filter(owner_id=request.user.id)
    check_box_list = request.POST.getlist('check_box_list')
    button_action = request.POST.get('button_list')
    folder_select = request.POST.get('folder_select')
    rl = Report.objects.filter(pk__in=check_box_list)
    if button_action == 'addfolder':
        for v in rl:
            v.folder_id = folder_select
            v.save()
    return render_to_response('user_report.html', {'report_list': report_list, 'full_name': request.user.username,
                                                   'rl': rl, 'fl': folder_list},
                              context_instance=RequestContext(request))

@login_required
def report_details(request, id):
   #x = request.GET.get('detail', '')
    r = Report.objects.get(pk=id)
    return render_to_response('report_details.html', {'r': r,'full_name': request.user.username}, context_instance=RequestContext(request))


@login_required
def delete(request, id):
    r = get_object_or_404(Report, pk=id).delete()
    return HttpResponseRedirect('/reports/list/')

@login_required
def report_all(request):
    public_reports = Report.objects.filter(private=False)
    if (request.user.groups.count() > 0):
        private_reports = Report.objects.none()
        group_list = request.user.groups.all()
        for g in group_list:
            users = User.objects.filter(groups__id=g.id)
            for u in users:
                temp = Report.objects.filter(user_id=u.id)
                private_reports = (private_reports | temp)
        all_reports = (public_reports | private_reports).distinct()
        return render_to_response('report_all.html',
                                  {'all': all_reports, 'full_name': request.user.username, 'groups': group_list},
                                  context_instance=RequestContext(request))
    else:
        return render_to_response('report_all.html', {'pr': public_reports,'full_name': request.user.username},
                                  context_instance=RequestContext(request))




#qs = SomeModel.objects.get(Q(some_attribute=something) | Q(some_other_attribute=something)).distinct()

@login_required
def new_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST,request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user_id = request.user.id
            profile.save()
            return HttpResponse('Thank you')
    else:
        form = ReportForm()
    return render_to_response('report.html', {'form_info': form,'full_name': request.user.username},
                              context_instance=RequestContext(request))

@login_required
def edit_report(request, id):
    my_record = Report.objects.get(pk=id)
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES, instance=my_record)
        if form.is_valid():
            form.save()
            return HttpResponse('Change Saved.')
    else:
        form = ReportForm(instance=my_record)
    return render_to_response('report_edit.html', {'form_info': form,'full_name': request.user.username},
                              context_instance=RequestContext(request))


def get_absolute_url(self):
        return self.image.url


def new_folder(request):
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            info = form.save(commit=False)
            info.owner_id = request.user.id
            info.save()
            return HttpResponse('New folder created')
    else:
        info = FolderForm()
    return render_to_response('new_folder.html', {'form_info': info, 'full_name': request.user.username},
                              context_instance=RequestContext(request))


def search_form(request):
    return render(request, 'search_form.html')


def search(request):
    search_select = request.GET.get('search_select')
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        reports = 0
        print(search_select)
        if search_select == 'subject':
            reports = Report.objects.filter(subject__icontains=q)
        if search_select == 'long_text':
            reports = Report.objects.filter(long_text__icontains=q)
        if search_select == 'short_text':
            reports = Report.objects.filter(short_text__icontains=q)
        if search_select == 'keywords':
            a = []
            a = q
           # print(a)
            for x in a:
                rlist = Report.objects.filter(kw__icontains=x)
                reports = list(chain(rlist))
        return render(request, 'search_results.html',
            {'Reports': reports, 'query': q})
    else:
        return render(request, 'search_form.html', {'error': True, 'full_name': request.user.username},
                      context_instance=RequestContext(request))


