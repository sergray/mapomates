import logging
import random
import urllib, urllib2

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import simplejson as json

from django_odesk.core.clients import RequestClient

from annoying.decorators import render_to, ajax_request

from mapomates.models import Provider, Team, Membership
from mapomates.odesk_helpers import get_user_reference, get_user_cipher_text


meanings = [
    "Two Brave Developers",
    "Twisted By Design",
    "There Be Dragons",
    "Two Business Days",
]


@render_to('home.html')
def home(request):
    """ Show map with users including authenticated user """
    query = request.GET
    profiles = []

    if request.user.is_authenticated:
        client = RequestClient(request)
        # TODO better caching
        if not 'cipher_text' in request.session:
            user_ref = get_user_reference(client)
            if user_ref:
                cipher_text = get_user_cipher_text(client, user_ref)
            else:
                cipher_text = ''
            request.session['cipher_text'] = cipher_text
        cipher_text = request.session['cipher_text']
        profiles.append(cipher_text)

    if query:
        url = 'http://www.odesk.com/api/profiles/v1/search/providers.json?'+\
                urllib.urlencode(request.GET)
        data = json.loads(urllib2.urlopen(url).read())
        if 'provider' in data['providers']:
            profiles += [prov['ciphertext'] for prov in data['providers']['provider']]
    tbd_meaning = random.choice(meanings)
    return {'tbd_meaning': tbd_meaning, 'profiles': json.dumps(profiles[:21])}


@ajax_request
def ajax_proxy(request):
    """
    A proxy method to bypass cross-domain AJAX restriction
    """
    url = urllib.unquote(request.GET['url'])
    data = urllib2.urlopen(url).read()
    return data


@login_required
@ajax_request
def users_list(request):
    user = request.user
    mates_list = []
    try:
        provider = Provider.objects.get(username=user.username)
    except Provider.DoesNotExist:
        # TODO queue update task and return message about pending result
        return mates_list
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
            }
        except Exception, exc:
            logging.error("Skipping mate_data for %r: %r" % (p, exc))
            continue
        mates_list.append(mate_data)
    return mates_list
