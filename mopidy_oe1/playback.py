from __future__ import unicode_literals

import logging

from client import OE1Client

from mopidy import backend

from mopidy_oe1.library import OE1LibraryUri, OE1UriType

logger = logging.getLogger(__name__)


class OE1PlaybackProvider(backend.PlaybackProvider):
    def __init__(self, audio, backend, client=OE1Client()):
        super(OE1PlaybackProvider, self).__init__(audio, backend)
        self.client = client

    def change_track(self, track):
        library_uri = OE1LibraryUri.parse(track.uri)
        if library_uri is None or\
           library_uri.uri_type != OE1UriType.ARCHIVE_ITEM:
            return False

        item = self.client.get_item(library_uri.day_id, library_uri.item_id)
        if item is None:
            return False

        track = track.copy(uri=item['url'])
        return super(OE1PlaybackProvider, self).change_track(track)
