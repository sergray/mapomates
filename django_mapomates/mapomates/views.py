from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import simplejson as json

from annoying.decorators import render_to

from mapomates.models import Provider, Team, Membership

@login_required
@render_to('home.html')
def home(request):
    """ Show map with users """
    return {}


def ajax_response(data):
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')
    

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
                'location': ', '.join([p.city, p.country]),
                #'coords': [float(p.lat), float(p.lon)],
                'coords': [0.0, 0.0],  # FIXME when lat, lon will be geocoded
            }
        except Exception, exc:
            logging.error("Skipping mate_data for %r: %r" % (p, exc))
            continue
        mates_list.append(mate_data)
    return ajax_response(mates_list)
