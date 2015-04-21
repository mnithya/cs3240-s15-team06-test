from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
               
               
    url(r'^$', 'polls.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),

               
    # user auth urls
    url(r'^accounts/login/$',  'polls.views.login'),
    url(r'^accounts/auth/$',  'polls.views.auth_view'),
    url(r'^accounts/logout/$', 'polls.views.logout'),
    url(r'^accounts/loggedin/$', 'polls.views.loggedin'),
    url(r'^accounts/invalid/$', 'polls.views.invalid_login'),
    url(r'^accounts/register/$', 'polls.views.register_user'),
    url(r'^accounts/register_success/$', 'polls.views.register_success'),
    
    # report
    url(r'^reports/new/$',  'polls.views.new_report'),
    url(r'^reports/list/$',  'polls.views.user_report'),
    url(r'^reports/detail/(?P<id>\d+)/$', 'polls.views.report_details'),
    url(r'^reports/delete/(?P<id>\d+)/$','polls.views.delete'),
    url(r'^reports/all/$','polls.views.report_all'),
    url(r'^reports/edit/(?P<id>\d+)/$', 'polls.views.edit_report'),
               
    # folder
    url(r'^folder/new/$', 'polls.views.new_folder'),
    
    #search
    url(r'^search-form/$', 'polls.views.search_form'),
    url(r'^search/$', 'polls.views.search'),
               
]
