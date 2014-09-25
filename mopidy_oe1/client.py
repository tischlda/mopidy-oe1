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
    base_uri = 'http://oe1.orf.at'
    today_uri = base_uri + '/programm/konsole/heute'
    day_uri = base_uri + '/programm/konsole/tag/%s'
    LIVE = "http://mp3stream3.apasf.apa.at:8000/listen.pls"
    CAMPUS = "http://mp3stream4.apasf.apa.at:8000/listen.pls"

    def __init__(self, http_client=HttpClient()):
        self.http_client = http_client

    def get_days(self):
        decoded_content = self._get_json(OE1Client.today_uri)
        if decoded_content is not None:
            return [_extract_day(day) for day in decoded_content['nav']]
        return []

    def get_day(self, day_id):
        decoded_content = self._get_json(OE1Client.day_uri % day_id)
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
            content = self.http_client.get(uri)
            decoder = simplejson.JSONDecoder()
            return decoder.decode(content)
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
