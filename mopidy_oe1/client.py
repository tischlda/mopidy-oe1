from __future__ import unicode_literals


import logging
import urllib2

from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

import dateutil.parser

import simplejson

logger = logging.getLogger(__name__)


class HttpClient(object):
    cache_opts = {
        'cache.type': 'memory',
    }

    cache = CacheManager(**parse_cache_config_options(cache_opts))

    @cache.cache('get', expire=60)
    def get(self, url):
        try:
            logger.info('Fetching data from \'%s\'.', url)
            response = urllib2.urlopen(url)
            content = response.read()
            encoding = response.headers['content-type'].split('charset')[-1]
            return unicode(content, encoding)
        except Exception, e:
            logger.error('Error fetching data from \'%s\': %s', url, e)

    def refresh(self):
        self.cache.invalidate(self.get, 'get')


class OE1Client(object):
    archive_uri = 'http://audioapi.orf.at/oe1/json/2.0/broadcasts/'
    record_uri = 'https://audioapi.orf.at/oe1/api/json/current/broadcast/%s/%s'
    item_uri = 'http://loopstream01.apa.at/?channel=oe1&shoutcast=0&id=%s'

    LIVE = "http://mp3stream3.apasf.apa.at:8000/listen.pls"
    CAMPUS = "http://mp3stream4.apasf.apa.at:8000/listen.pls"

    def __init__(self, http_client=HttpClient()):
        self.http_client = http_client

    def get_days(self):

        def to_day(rec):
            return {
                'id': _get_day_id(rec),
                'label': _get_day_label(rec)
            }

        json = self._get_archive_json()
        if json is not None:
            return [to_day(rec) for rec in reversed(json)]
        return []

    def get_day(self, day_id):

        def to_item(i, rec):
            time = dateutil.parser.parse(rec['startISO'])

            return {
                'id': str(i),
                'time': time.strftime("%H:%M:%S"),
                'title': rec['title'],
            }

        day_rec = self._get_day_json(day_id)
        records = day_rec['broadcasts']

        return {
                'id': day_id,
                'label': _get_day_label(day_rec),
                'items': [to_item(i, rec) for i, rec in enumerate(records)]
        }

    def get_item(self, day_id, item_id):
        day = self.get_day(day_id)
        return next(item for item in day['items'] if item['id'] == item_id)

    def get_item_url(self, day_id, item_id):
        day_rec = self._get_day_json(day_id)

        item_id = int(item_id)
        item_rec = day_rec['broadcasts'][item_id]

        json = self._get_record_json(item_rec['programKey'], day_id)

        streams = json['streams']
        if len(streams) == 0:
            return ""

        streamId = streams[0]['loopStreamId']
        return OE1Client.item_uri % streamId

    def refresh(self):
        self.http_client.refresh()

    def _get_json(self, uri):
        try:
            content = self.http_client.get(uri)
            decoder = simplejson.JSONDecoder()
            return decoder.decode(content)
        except Exception, e:
            logger.error('Error decoding content received from \'%s\': %s',
                         uri, e)

    def _get_archive_json(self):
        return self._get_json(OE1Client.archive_uri)

    def _get_day_json(self, day_id):
        json = self._get_archive_json()
        return next(rec for rec in json if _get_day_id(rec) == day_id)

    def _get_record_json(self, programKey, day):
        return self._get_json(OE1Client.record_uri % (programKey, day))


def _get_day_id(day_rec):
    return str(day_rec['day'])


def _get_day_label(day_rec):
    time = dateutil.parser.parse(day_rec['dateISO'])
    return time.strftime("%a %d. %b %Y")
