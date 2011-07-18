""" Varios function implementing integration with oDesk API 

>>> import logging
>>> logging.basicConfig(loglevel=logging.DEBUG)
>>> from django.contrib.sessions.models import Session
>>> s = Session.objects.all()[0]
>>> api_token = s.get_decoded()['_odesk_api_token']
>>> from django_odesk.core.clients import DefaultClient
>>> cli = DefaultClient(api_token)
>>> from mapomates.odesk_helpers import sync_teams, sync_team_users, sync_user_profile
>>> for t in sync_teams(cli):
...     users = sync_team_users(cli, t.reference)
>>> from mapomates.models import Provider
>>> from mapomates.geo_helpers import get_coords
>>> for u in Provider.objects.all():
...     sync_user_profile(cli, u.reference)
...     update_profile_coords(u, get_coords(u.location))
>>> len(Provider.objects.all()) > 0
True
"""

import logging
import uuid
import urlparse


from django.db import models, transaction

from mapomates.models import Team, Provider, Membership


@transaction.commit_on_success
def update_team(oteam):
    try:
        team = Team.objects.get(reference=oteam['reference'])
    except Team.DoesNotExist:
        team = Team.objects.create(
            name=oteam['name'],
            reference=oteam['reference'],
        )
    else:
        if team.name != oteam['name']:
            team.name = oteam['name']
            team.save()
    return team


def sync_teams(client):
    teams = []
    try:
        odesk_teams = client.hr.get_teams()
    except Exception, exc:
        logging.error("Could not fetch user teams: %r" % exc)
        return teams
    for oteam in odesk_teams:
        teams.append(update_team(oteam))
    # TODO delete old teams
    return teams


@transaction.commit_on_success
def update_team_user(team, ouser, update_id):
    try:
        provider = Provider.objects.get(reference=ouser['reference'])
    except Provider.DoesNotExist:
        provider = Provider.objects.create(
            name=' '.join([ouser['first_name'], ouser['last_name']]),
            reference=ouser['reference'],
            username=ouser['email'],
            profile_url=ouser['public_url'],
        )
    finally:
        try:
            relation = Membership.objects.filter(
                team=team,
                provider=provider,
            )[0]
        except IndexError:
            relation = Membership.objects.create(
                team=team,
                provider=provider,
                update_id=update_id,
            )
        else:
            relation.update_id = update_id
            relation.save()
    return provider
    

def sync_team_users(client, team_reference):
    providers = []
    try:
        team = Team.objects.get(reference=team_reference)
    except Team.DoesNotExist:
        logging.error("Team %r does not exist" % team_reference)
        return providers
    try:
        odesk_users = client.hr.get_team_users(team_reference)
    except Exception, exc:
        logging.error(
            "Failed to fetch %r team users: %r" % (team_reference, exc)
        )
        return providers
    update_id = uuid.uuid4().hex
    for ouser in odesk_users:
        providers.append(update_team_user(team, ouser, update_id))
    # remove deleted relations
    Membership.objects.filter(
        team=team
    ).filter(
        ~models.Q(update_id=update_id)
    ).delete()
    return providers


@transaction.commit_on_success
def update_profile(provider, oprofile):
    attr2key = (
        ('portrait_url', 'dev_portrait'),
        ('city', 'dev_city'),
        ('country', 'dev_country'),
    )
    for a, k in attr2key:
        setattr(provider, a, oprofile[k])
    provider.save()


@transaction.commit_manually
def update_profile_coords(provider, coords):
    try:
        provider.lat, provider.lon = coords
    except Exception, exc:
        logging.error(
            'failed set coords %r to provider %r: %r' % (
                coords, provider, exc
            )
        )
        transaction.rollback()
    else:
        transaction.commit()


def sync_user_profile(client, user_reference):
    try:
        provider = Provider.objects.get(reference=user_reference)
    except Provider.DoesNotExist:
        logger.error("Provider %r does not exist" % user_reference)
        return
    cipher_text = provider.cipher_text
    try:
        oprofile = client.provider.get_provider(cipher_text)
    except Exception, exc:
        logging.error("Failed to get provider for %r: %r" % (cipher_text, exc))
        return
    update_profile(provider, oprofile)


def get_user_reference(client):
    """ Return reference for user of oDesk client """
    role = None
    try:
        role = client.hr.get_user_role()['userrole'][0]
    except Exception, exc:
        logging.error('Failed to get role: %r' % (exc,))
        return role
    return role['user__reference']


def get_cipher_text(public_url):
    path = urlparse.urlsplit(public_url).path
    cipher = path.split('/')[-1]
    return cipher


def get_user_cipher_text(client, reference):
    """ Return cipher text for user of oDesk client """
    user = client.hr.get_user(reference)
    public_url = user['public_url']
    return get_cipher_text(public_url)
