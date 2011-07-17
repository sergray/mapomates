from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('profiles.views',
    url('^profile/(?P<cipher_text>.*?)/', 'profile', name='profile-resource'),
)
