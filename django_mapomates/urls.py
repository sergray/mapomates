from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^odesk_auth/', include('django_odesk.auth.urls')),
    url(r'', include('mapomates.urls')),
    # Examples:
    # url(r'^$', 'django_mapomates.views.home', name='home'),
    # url(r'^django_mapomates/', include('django_mapomates.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
