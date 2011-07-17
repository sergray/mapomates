import logging
import random
import urllib, urllib2

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import simplejson as json

from annoying.decorators import render_to

from mapomates.models import Provider, Team, Membership

meanings = [
    "Two Brave Developers",
    "Twisted By Design",
    "There Be Dragons",
    "Two Business Days",
]

@login_required
@render_to('home.html')
def home(request):
    """ Show map with users """
    query = request.GET
    profiles = []
    if query:
        url = 'http://www.odesk.com/api/profiles/v1/search/providers.json?'+\
                urllib.urlencode(request.GET)
        data = json.loads(urllib2.urlopen(url).read())
        profiles = [prov['ciphertext'] for prov in data['providers']['provider']]
    tbd_meaning = random.choice(meanings) 
    return {'tbd_meaning': tbd_meaning, 'profiles': json.dumps(profiles[:10])}


def ajax_response(data):
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def ajax_proxy(request):
    """
    A proxy method to bypass cross-domain AJAX restriction
    """
    url = urllib.unquote(request.GET['url'])
    data = urllib2.urlopen(url).read()
    return ajax_response(data)

@login_required
def users_list(request):
    user = request.user
    mates_list = []
    try:
        provider = Provider.objects.get(username=user.username)
    except Provider.DoesNotExist:
        # TODO queue update task and return message about pending result
        return ajax_response(mates_list)
    providers = Provider.objects.filter(
        teams__in=provider.teams.all()
    ).defer('teams')
    for p in providers:
        try:
            # lat, lon are stored as strings, so there might be an exception
            mate_data = {
                'name': p.name,
                'username': p.username,
                'pic': p.portrait_url,
                'location': p.location,
                'coords': [float(p.lat), float(p.lon)],
                #'coords': [0.0, 0.0],  # FIXME when lat, lon will be geocoded
            }
        except Exception, exc:
            logging.error("Skipping mate_data for %r: %r" % (p, exc))
            continue
        mates_list.append(mate_data)
    return ajax_response(mates_list)
