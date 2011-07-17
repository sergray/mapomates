from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('mapomates.views',
    url('^$', 'home', name='home'),
    url('proxy/$', 'ajax_proxy', name='ajax_proxy'),
    url('profiles.json', 'users_list', name='all-json-profiles'),
)
