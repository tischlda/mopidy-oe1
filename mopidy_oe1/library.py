from __future__ import unicode_literals

import logging

from client import OE1Client

from mopidy import backend
from mopidy.models import Ref, Track

logger = logging.getLogger(__name__)


class OE1LibraryProvider(backend.LibraryProvider):
    root_directory = Ref.directory(uri='oe1:directory', name='OE1')

    def __init__(self, *args, **kwargs):
        super(OE1LibraryProvider, self).__init__(*args, **kwargs)

        self.client = OE1Client()

        self._root = [
            Ref.directory(uri='oe1:live', name='Live'),
            Ref.directory(uri='oe1:archive', name='7 Tage')]

    def browse(self, uri):
        print uri
        if uri == self.root_directory.uri:
            return self._root

        if uri == 'oe1:archive':
            return [Ref.directory(uri='oe1:day/' + day['id'], name=day['label']) for day in self.client.get_days()]

        if uri[:8] == 'oe1:day/':
            day_id = uri[8:16]
            item_id = uri[17:]
            print '  day_id: ' + day_id
            print '  item_id: ' + item_id
            if item_id != '':
                item = self.client.get_item(day_id, item_id)
                return Track(uri='oe1:day/' + day_id + '/' + item['id'], name=item['title'], url=item['url'])
            else:
                return [Ref.track(uri='oe1:day/' + day_id + '/' + item['id'], name=item['title']) for item in self.client.get_day(day_id)['items']]

    def find_exact(self, query=None, uris=None):
        return []

    def lookup(self, uri):
        if uri[:8] == 'oe1:day/':
            day_id = uri[8:16]
            item_id = uri[17:]
            print '  day_id: ' + day_id
            print '  item_id: ' + item_id
            if item_id != '':
                item = self.client.get_item(day_id, item_id)
                return [Track(uri='oe1:day/' + day_id + '/' + item['id'], name=item['title'])]

    def refresh(self, uri=None):
        pass

    def search(self, query=None, uris=None):
        return []
