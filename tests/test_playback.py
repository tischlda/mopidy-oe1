from __future__ import unicode_literals

import unittest

from mopidy.models import Track

from mock import Mock

from mopidy_oe1.client import OE1Client
from mopidy_oe1.playback import OE1PlaybackProvider, OE1LibraryUri, OE1UriType


class OE1LibraryUriTest(unittest.TestCase):
    def test_playback_archive_item(self):
        library_uri = OE1LibraryUri(OE1UriType.ARCHIVE_ITEM, '20140914', '1234567')
        track = Track(uri=str(library_uri))

        client_mock = Mock()
        client_mock.get_item = Mock(return_value={'url': 'result_uri'})

        audio_mock = Mock()
        audio_mock.set_uri = Mock()

        playback = OE1PlaybackProvider(audio_mock, None, client=client_mock)
        result = playback.change_track(track)

        self.assertTrue(result)
        self.assertEqual(audio_mock.set_uri.call_count, 1)
        self.assertEqual(audio_mock.set_uri.call_args[0][0], 'result_uri')

    def test_playback_live(self):
        library_uri = OE1LibraryUri(OE1UriType.LIVE)
        track = Track(uri=str(library_uri))

        audio_mock = Mock()
        audio_mock.set_uri = Mock()

        playback = OE1PlaybackProvider(audio_mock, None, client=None)
        result = playback.change_track(track)

        self.assertTrue(result)
        self.assertEqual(audio_mock.set_uri.call_count, 1)
        self.assertEqual(audio_mock.set_uri.call_args[0][0], OE1Client.LIVE)

    def test_playback_campus(self):
        library_uri = OE1LibraryUri(OE1UriType.CAMPUS)
        track = Track(uri=str(library_uri))

        audio_mock = Mock()
        audio_mock.set_uri = Mock()

        playback = OE1PlaybackProvider(audio_mock, None, client=None)
        result = playback.change_track(track)

        self.assertTrue(result)
        self.assertEqual(audio_mock.set_uri.call_count, 1)
        self.assertEqual(audio_mock.set_uri.call_args[0][0], OE1Client.CAMPUS)

    def test_playback_invalid_url(self):
        track = Track(uri='invalid')

        audio_mock = Mock()
        audio_mock.set_uri = Mock()

        playback = OE1PlaybackProvider(audio_mock, None, client=None)
        result = playback.change_track(track)

        self.assertFalse(result)
        self.assertEqual(audio_mock.set_uri.call_count, 0)

    def test_playback_unplayable_url(self):
        library_uri = OE1LibraryUri(OE1UriType.ARCHIVE)
        track = Track(uri=str(library_uri))

        audio_mock = Mock()
        audio_mock.set_uri = Mock()

        playback = OE1PlaybackProvider(audio_mock, None, client=None)
        result = playback.change_track(track)

        self.assertFalse(result)
        self.assertEqual(audio_mock.set_uri.call_count, 0)