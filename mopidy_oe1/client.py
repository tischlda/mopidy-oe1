from __future__ import unicode_literals


import logging
import urllib2

import simplejson

logger = logging.getLogger(__name__)


class HttpClient(object):
    def get(self, url):
        try:
            response = urllib2.urlopen(url)
            content = response.read()
            encoding = response.headers['content-type'].split('charset')[-1]
            return unicode(content, encoding)
        except Exception, e:
            logger.error('Error fetching data from \'%s\': %s', url, e)


class OE1Client(object):
    def __init__(self, http_client=HttpClient()):
        self.cache = {}
        self.http_client = http_client
        self.base_uri = 'http://oe1.orf.at'
        self.entry_point = '/programm/konsole/heute'

    def get_days(self):
        uri = self.base_uri + self.entry_point
        decoded_content = self._get_json(uri)
        if decoded_content is not None:
            return [_extract_day(day) for day in decoded_content['nav']]
        return []

    def get_day(self, day_id):
        decoded_content = self._get_json('%s/programm/konsole/tag/%s'
                                         % (self.base_uri, day_id))
        if decoded_content is not None:
            return {
                'id': day_id,
                'label': decoded_content['day_label'],
                'items': [_extract_item(item)
                          for item in decoded_content['list']]
            }

    def get_item(self, day_id, item_id):
        day = self.get_day(day_id)
        return next(item for item in day['items'] if item['id'] == item_id)

    def _get_json(self, uri):
        try:
            if uri not in self.cache:
                content = self.http_client.get(uri)
                decoder = simplejson.JSONDecoder()
                self.cache[uri] = decoder.decode(content)
            return self.cache[uri]
        except Exception, e:
            logger.error('Error decoding content received from \'%s\': %s',
                         uri, e)


def _extract_day_id(url):
    return url[22:]


def _extract_day(day):
    return {
        'id': _extract_day_id(day['url']),
        'label': day['day_label']
    }


def _extract_item(item):
    return {
        'id': item['id'],
        'time': item['time'],
        'title': item['title'],
        'url': item['url_stream']
    }
