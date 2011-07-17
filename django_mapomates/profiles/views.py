import logging

from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.forms.models import model_to_dict

from django_odesk.core.clients import RequestClient

from annoying.decorators import ajax_request

from mapomates.geo_helpers import get_coords

from profiles.models import Profile
from profiles.forms import ProfileForm


@require_http_methods(['GET'])
def get_profile(request, cipher_text):
    try:
        profile = Profile.objects.get(cipher_text=cipher_text)
    except Profile.DoesNotExist:
        client = RequestClient(request)
        # TODO run asynchronously
        try:
            provider = client.provider.get_provider(cipher_text)
        except Exception, exc:
            logging.error(
                "get_provider for %r failed: %r" % (
                    cipher_text,
                    exc
            ))
            return HttpResponseBadRequest()
        location = ', '.join([
            provider['dev_city'],
            provider['dev_country'],
        ])
        # TODO run asynchronously
        lat, lon = get_coords(location)
        profile = Profile.objects.create(
            cipher_text=cipher_text,
            full_name=provider['dev_full_name'],
            portrait=provider['dev_portrait_50'],
            location = location,
            lat=lat,
            lon=lon,
        )
    return model_to_dict(profile)


@require_http_methods(['POST'])
def post_profile(request, cipher_text):
    try:
        profile = Profile.objects.get(cipher_text=cipher_text)
    except Profile.DoesNotExist:
        profile = Profile(cipher_text=cipher_text)
    profile_form = ProfileForm(request.POST, instance=profile)
    if profile_form.is_valid():
        profile_form.save()
        return {'status': 'ok'}
    else:
        logging.error(profile_form.errors)
        return HttpResponseBadRequest()


PROFILE_HANDLERS = {
    'GET': get_profile,
    'POST': post_profile,
}


@ajax_request
def profile(request, cipher_text):
    handler = PROFILE_HANDLERS.get(request.method, None)
    if not handler:
        logging.warning('Bad request: %r' % request.method)
        return HttpResponseBadRequest()
    else:
        return handler(request, cipher_text)
