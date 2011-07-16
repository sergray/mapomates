import urlparse

from django.db import models


class OdeskObject(models.Model):
    name = models.CharField(max_length=80)
    reference = models.CharField(max_length=48, db_index=True, unique=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return u"%s reference=%s" % (self.name, self.reference)


class Team(OdeskObject):
    pass
    

class Provider(OdeskObject):
    username = models.CharField(max_length=80, unique=True, db_index=True)
    city = models.CharField(max_length=80, blank=True, default='')
    country = models.CharField(max_length=80, blank=True, default='')
    profile_url = models.URLField(verify_exists=False, blank=True)
    portrait_url = models.URLField(verify_exists=False, blank=True)
    teams = models.ManyToManyField(
        Team, related_name='providers', blank=True, through='Membership'
    )
    lat = models.CharField(max_length=20, blank=True, default='')
    lon = models.CharField(max_length=20, blank=True, default='')

    def __unicode__(self):
        return u" ".join([
            super(Provider, self).__unicode__(),
            u"username=%s country=%r city=%r" % (
                self.username, self.country, self.city
            )
        ])

    @property
    def cipher_text(self):
        path = urlparse.urlsplit(self.profile_url).path
        cipher = path.split('/')[-1]
        return cipher


class Membership(models.Model):
    team = models.ForeignKey(Team)
    provider = models.ForeignKey(Provider)
    update_id = models.CharField(
        max_length=32, db_index=True, blank=True, default=''
    )
