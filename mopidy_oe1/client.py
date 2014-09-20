from __future__ import unicode_literals

import json
import logging

logger = logging.getLogger(__name__)


class OE1Client(object):
    def __init__(self, http_client):
        self.http_client = http_client
        self.base_uri = 'http://oe1.orf.at'
        self.entry_point = '/programm/konsole/heute'

    def get_days(self):
        content = self.http_client.get(self.base_uri + self.entry_point)
        decoder = json.JSONDecoder()
        decoded_content = decoder.decode(content)

        return [_extract_day(day) for day in decoded_content['nav']]

    def get_day(self, id):
        content = self.http_client.get(self.base_uri + '/programm/tag/' + id)
        decoder = json.JSONDecoder()
        decoded_content = decoder.decode(content)

        return {'id': id, 'label': decoded_content['day_label']}


def _extract_day_id(url):
    return url[22:]


def _extract_day(day):
    return {
        'id': _extract_day_id(day['url']),
        'label': day['day_label']
    }
