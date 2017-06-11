from __future__ import unicode_literals

import unittest

from mock import Mock

from mopidy_oe1.client import OE1Client
from mopidy_oe1.playback import OE1LibraryUri, OE1PlaybackProvider, OE1UriType


class OE1LibraryUriTest(unittest.TestCase):
    def test_playback_archive_item(self):
        library_uri = OE1LibraryUri(OE1UriType.ARCHIVE_ITEM,
                                    '20140914', '1234567')
        client_mock = Mock()
        client_mock.get_item_url = Mock(return_value='result_uri')
        playback = OE1PlaybackProvider(None, None, client=client_mock)

        result = playback.translate_uri(str(library_uri))

        self.assertEqual(result, 'result_uri')

    def test_playback_live(self):
        library_uri = OE1LibraryUri(OE1UriType.LIVE)
        playback = OE1PlaybackProvider(None, None, client=None)

        result = playback.translate_uri(str(library_uri))

        self.assertEqual(result, OE1Client.LIVE)

    def test_playback_campus(self):
        library_uri = OE1LibraryUri(OE1UriType.CAMPUS)
        playback = OE1PlaybackProvider(None, None, client=None)

        result = playback.translate_uri(str(library_uri))

        self.assertEqual(result, OE1Client.CAMPUS)

    def test_playback_invalid_url(self):
        audio_mock = Mock()
        audio_mock.set_uri = Mock()

        playback = OE1PlaybackProvider(audio_mock, None, client=None)
        result = playback.translate_uri('invalid')

        self.assertIsNone(result)

    def test_playback_unplayable_url(self):
        library_uri = OE1LibraryUri(OE1UriType.ARCHIVE)
        playback = OE1PlaybackProvider(None, None, client=None)

        result = playback.translate_uri(str(library_uri))

        self.assertIsNone(result)
