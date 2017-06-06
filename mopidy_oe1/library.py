from __future__ import unicode_literals

import logging
import re

from client import OE1Client

from mopidy import backend
from mopidy.models import Ref, Track

logger = logging.getLogger(__name__)


class OE1Uris(object):
    ROOT = 'oe1:directory'
    LIVE = 'oe1:live'
    CAMPUS = 'oe1:campus'
    ARCHIVE = 'oe1:archive'


class OE1LibraryProvider(backend.LibraryProvider):
    root_directory = Ref.directory(uri=OE1Uris.ROOT, name='OE1')
    root = [
        Ref.track(uri=OE1Uris.LIVE, name='Live'),
        Ref.track(uri=OE1Uris.CAMPUS, name='Campus'),
        Ref.directory(uri=OE1Uris.ARCHIVE, name='7 Tage')]

    def __init__(self, backend, client=OE1Client()):
        super(OE1LibraryProvider, self).__init__(backend)
        self.client = client

    def browse(self, uri):
        try:
            library_uri = OE1LibraryUri.parse(uri)
        except InvalidOE1Uri, e:
            logger.error(e)
            return []

        if library_uri.uri_type == OE1UriType.ROOT:
            return self.root

        if library_uri.uri_type == OE1UriType.ARCHIVE:
            return self._browse_archive()

        if library_uri.uri_type == OE1UriType.ARCHIVE_DAY:
            return self._browse_day(library_uri.day_id)

        logger.warn('OE1LibraryProvider.browse called with uri '
                    'that does not support browsing: \'%s\'.' % uri)
        return []

    def _browse_archive(self):
        return [Ref.directory(uri=str(OE1LibraryUri(OE1UriType.ARCHIVE_DAY,
                                                    day['id'])),
                              name=day['label'])
                for day in self.client.get_days()]

    def _get_track_title(self, item):
        return '%s: %s' % (item['time'], item['title'])

    def _browse_day(self, day_id):
        return [Ref.track(uri=str(OE1LibraryUri(OE1UriType.ARCHIVE_ITEM,
                                                day_id, item['id'])),
                          name=self._get_track_title(item))
                for item in self.client.get_day(day_id)['items']]

    def lookup(self, uri):
        try:
            library_uri = OE1LibraryUri.parse(uri)
        except InvalidOE1Uri, e:
            logger.error(e)
            return []

        if library_uri.uri_type == OE1UriType.LIVE:
            return [Track(uri=OE1Uris.LIVE, name='Live')]

        if library_uri.uri_type == OE1UriType.CAMPUS:
            return [Track(uri=OE1Uris.CAMPUS, name='Campus')]

        if library_uri.uri_type == OE1UriType.ARCHIVE_DAY:
            return self._browse_day(library_uri.day_id)

        if library_uri.uri_type == OE1UriType.ARCHIVE_DAY:
            return self._browse_day(library_uri.day_id)

        if library_uri.uri_type == OE1UriType.ARCHIVE_ITEM:
            return self._lookup_item(library_uri.day_id, library_uri.item_id)

        logger.warn('OE1LibraryProvider.lookup called with uri '
                    'that does not support lookup: \'%s\'.' % uri)
        return []

    def _lookup_item(self, day_id, item_id):
        item = self.client.get_item(day_id, item_id)
        return [Track(uri=str(OE1LibraryUri(OE1UriType.ARCHIVE_ITEM,
                                            day_id, item['id'])),
                      name=self._get_track_title(item))]

    def refresh(self, uri=None):
        self.client.refresh()


class OE1LibraryUri(object):
    def __init__(self, uri_type, day_id=None, item_id=None):
        self.uri_type = uri_type
        self.day_id = day_id
        self.item_id = item_id

    archive_parse_expression = '^' + re.escape(OE1Uris.ARCHIVE) +\
                               ':(?P<day_id>\d{8})(:(?P<item_id>\d+))?$'
    archive_parser = re.compile(archive_parse_expression)

    @staticmethod
    def parse(uri):
        if uri == OE1Uris.ROOT:
            return OE1LibraryUri(OE1UriType.ROOT)
        if uri == OE1Uris.LIVE:
            return OE1LibraryUri(OE1UriType.LIVE)
        if uri == OE1Uris.CAMPUS:
            return OE1LibraryUri(OE1UriType.CAMPUS)
        if uri == OE1Uris.ARCHIVE:
            return OE1LibraryUri(OE1UriType.ARCHIVE)

        matches = OE1LibraryUri.archive_parser.match(uri)

        if matches is not None:
            day_id = matches.group('day_id')
            item_id = matches.group('item_id')

            if day_id is not None:
                if matches.group('item_id') is not None:
                    return OE1LibraryUri(OE1UriType.ARCHIVE_ITEM,
                                         day_id, item_id)
                return OE1LibraryUri(OE1UriType.ARCHIVE_DAY, day_id)
        raise InvalidOE1Uri(uri)

    def __str__(self):
        if self.uri_type == OE1UriType.ROOT:
            return OE1Uris.ROOT
        if self.uri_type == OE1UriType.LIVE:
            return OE1Uris.LIVE
        if self.uri_type == OE1UriType.CAMPUS:
            return OE1Uris.CAMPUS
        if self.uri_type == OE1UriType.ARCHIVE:
            return OE1Uris.ARCHIVE
        if self.uri_type == OE1UriType.ARCHIVE_DAY:
            return OE1Uris.ARCHIVE + ':' + self.day_id
        if self.uri_type == OE1UriType.ARCHIVE_ITEM:
            return OE1Uris.ARCHIVE + ':' + self.day_id + ':' + self.item_id


class InvalidOE1Uri(TypeError):
    def __init__(self, uri):
        super(TypeError, self).__init__(
            'The URI is not a valid OE1LibraryUri: \'%s\'.' % uri)


class OE1UriType(object):
    ROOT = 0
    LIVE = 1
    CAMPUS = 2
    ARCHIVE = 3
    ARCHIVE_DAY = 4
    ARCHIVE_ITEM = 5
