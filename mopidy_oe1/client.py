from __future__ import unicode_literals

import json
import logging
import urllib2

logger = logging.getLogger(__name__)


class HttpClient(object):
    def __init__(self):
        self.cache = {}

    def get(self, url):
        logger.debug(url)
        if not url in self.cache:
            self.cache[url] = urllib2.urlopen(url).read()
        return self.cache[url]


class OE1Client(object):
    def __init__(self, http_client=HttpClient()):
        self.http_client = http_client
        self.base_uri = 'http://oe1.orf.at'
        self.entry_point = '/programm/konsole/heute'

    def get_days(self):
        content = self.http_client.get(self.base_uri + self.entry_point)
        decoder = json.JSONDecoder()
        decoded_content = decoder.decode(content)

        return [_extract_day(day) for day in decoded_content['nav']]

    def get_day(self, day_id):
        content = self.http_client.get(self.base_uri + '/programm/konsole/tag/' + day_id)
        decoder = json.JSONDecoder()
        decoded_content = decoder.decode(content)

        return {
            'id': day_id,
            'label': decoded_content['day_label'],
            'items': [_extract_item(item) for item in decoded_content['list']]
        }

    def get_item(self, day_id, item_id):
        day = self.get_day(day_id)
        return next(item for item in day['items'] if item['id'] == item_id)

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
