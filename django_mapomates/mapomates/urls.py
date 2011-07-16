from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('mapomates.views',
    url('^$', 'home', name='home'),
)
