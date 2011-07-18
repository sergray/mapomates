import urllib
import urllib2
from django.utils import simplejson as json
import logging

def get_nominatim_data(loc_string, format='json'):
    """
    >>> data = get_nominatim_data("Odesa, Ukraine")
    >>> '46.4713468' in data
    True
    """
    query = urllib.urlencode({'q': loc_string, 'format': format})
    url = "http://nominatim.openstreetmap.org/search?%s" % query 
    data = urllib2.urlopen(url).read()
    return data


def get_coords(loc_string):
    """
    Takes location string and converts to coordinates

    TODO: Don't test for exact strings, because the precision may change.
    Test for numbers with some precision instead

    >>> get_coords("Odesa, Ukraine")
    ('46.4713468', '30.7296333')
    >>> get_coords("Nizhniy Novgorod, Russia")
    ('56.2970578445959', '44.0681708369552')
    >>> get_coords("221B Baker Street, London, UK")
    ('51.5237987', '-0.1584539')
    """
    data = json.loads(get_nominatim_data(loc_string, 'json'))
    try:
        coords = str(data[0]['lat']), str(data[0]['lon'])
    except Exception, exc:
        logging.error('get_coords failed for %r with %r: %r' % (loc_string, data, exc))
        coords = ['', '']
    return coords


if __name__ == "__main__":
    import doctest
    doctest.testmod()
