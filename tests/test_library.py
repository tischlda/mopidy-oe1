from __future__ import unicode_literals

import unittest

from mock import Mock

from mopidy.models import Ref

from mopidy_oe1.library import OE1LibraryProvider, OE1LibraryUri, OE1UriType


class OE1LibraryUriTest(unittest.TestCase):
    def test_parse_root_uri(self):
        uri = 'oe1:directory'
        result = OE1LibraryUri.parse(uri)
        self.assertEqual(result.uri_type, OE1UriType.ROOT)

    def test_parse_live_uri(self):
        uri = 'oe1:live'
        result = OE1LibraryUri.parse(uri)
        self.assertEqual(result.uri_type, OE1UriType.LIVE)

    def test_parse_campus_uri(self):
        uri = 'oe1:campus'
        result = OE1LibraryUri.parse(uri)
        self.assertEqual(result.uri_type, OE1UriType.CAMPUS)

    def test_parse_archive_uri(self):
        uri = 'oe1:archive'
        result = OE1LibraryUri.parse(uri)
        self.assertEqual(result.uri_type, OE1UriType.ARCHIVE)

    def test_parse_day_uri(self):
        uri = 'oe1:archive:20140914'
        result = OE1LibraryUri.parse(uri)
        self.assertEqual(result.uri_type, OE1UriType.ARCHIVE_DAY)
        self.assertEqual(result.day_id, '20140914')

    def test_parse_invalid_uri(self):
        uri = 'foo:bar'
        self.assertRaises(TypeError, OE1LibraryUri.parse, uri)

    def test_parse_item_uri(self):
        uri = 'oe1:archive:20140914:382176'
        result = OE1LibraryUri.parse(uri)
        self.assertEqual(result.uri_type, OE1UriType.ARCHIVE_ITEM)
        self.assertEqual(result.day_id, '20140914')
        self.assertEqual(result.item_id, '382176')

    def test_create_root_uri(self):
        parsed_uri = OE1LibraryUri(OE1UriType.ROOT)
        self.assertEqual(str(parsed_uri), 'oe1:directory')

    def test_create_live_uri(self):
        parsed_uri = OE1LibraryUri(OE1UriType.LIVE)
        self.assertEqual(str(parsed_uri), 'oe1:live')

    def test_create_campus_uri(self):
        parsed_uri = OE1LibraryUri(OE1UriType.CAMPUS)
        self.assertEqual(str(parsed_uri), 'oe1:campus')

    def test_create_archive_uri(self):
        parsed_uri = OE1LibraryUri(OE1UriType.ARCHIVE)
        self.assertEqual(str(parsed_uri), 'oe1:archive')

    def test_create_day_uri(self):
        parsed_uri = OE1LibraryUri(OE1UriType.ARCHIVE_DAY, '20140914')
        self.assertEqual(str(parsed_uri), 'oe1:archive:20140914')

    def test_create_item_uri(self):
        parsed_uri = OE1LibraryUri(OE1UriType.ARCHIVE_ITEM,
                                   '20140914', '382176')
        self.assertEqual(str(parsed_uri), 'oe1:archive:20140914:382176')


class OE1LibraryProviderTest(unittest.TestCase):
    def setUp(self):
        self.client_mock = Mock()
        self.client_mock.get_days = Mock(
            return_value=[
                {'id': '1', 'label': 'Day1'},
                {'id': '2', 'label': 'Day2'}
            ]
        )
        self.client_mock.get_day = Mock(
            return_value={
                'items': [
                    {'id': '1', 'time': '01:00', 'title': 'Item1'},
                    {'id': '2', 'time': '02:00', 'title': 'Item2'},
                    {'id': '3', 'time': '03:00', 'title': 'Item3'}
                ]
            }
        )
        self.client_mock.get_item = Mock(
            return_value={'id': '1', 'time': '01:00', 'title': 'Item1'}
        )

        self.library = OE1LibraryProvider(None, client=self.client_mock)

    def test_browse_invalid_uri(self):
        uri = 'foo:bar'
        result = self.library.browse(uri)
        self.assertEqual(result, [])

    def test_browse_unbrowsable_uri(self):
        uri = str(OE1LibraryUri(OE1UriType.LIVE))
        result = self.library.browse(uri)
        self.assertEqual(result, [])

    def test_browse_root(self):
        uri = str(OE1LibraryUri(OE1UriType.ROOT))
        result = self.library.browse(uri)
        self.assertEqual(len(result), 3)

    def test_browse_archive(self):
        uri = str(OE1LibraryUri(OE1UriType.ARCHIVE))
        result = self.library.browse(uri)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].type, Ref.DIRECTORY)
        self.assertEqual(result[0].uri, 'oe1:archive:1')
        self.assertEqual(result[0].name, 'Day1')

    def test_browse_archive_day(self):
        uri = str(OE1LibraryUri(OE1UriType.ARCHIVE_DAY, '20140914'))
        result = self.library.browse(uri)
        self.client_mock.get_day.assert_called_once_with('20140914')
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].type, Ref.TRACK)
        self.assertEqual(result[0].uri, 'oe1:archive:20140914:1')
        self.assertEqual(result[0].name, '01:00: Item1')

    def test_lookup_invalid_uri(self):
        uri = 'foo:bar'
        result = self.library.lookup(uri)
        self.assertEqual(result, [])

    def test_browse_unlookable_uri(self):
        uri = str(OE1LibraryUri(OE1UriType.ROOT))
        result = self.library.lookup(uri)
        self.assertEqual(result, [])

    def test_lookup_live(self):
        uri = str(OE1LibraryUri(OE1UriType.LIVE))
        result = self.library.lookup(uri)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].uri, uri)
        self.assertEqual(result[0].name, 'Live')

    def test_lookup_campus(self):
        uri = str(OE1LibraryUri(OE1UriType.CAMPUS))
        result = self.library.lookup(uri)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].uri, uri)
        self.assertEqual(result[0].name, 'Campus')

    def test_lookup_archive_day(self):
        uri = str(OE1LibraryUri(OE1UriType.ARCHIVE_DAY, '20140914'))
        result = self.library.lookup(uri)
        self.client_mock.get_day.assert_called_once_with('20140914')
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].type, Ref.TRACK)
        self.assertEqual(result[0].uri, 'oe1:archive:20140914:1')
        self.assertEqual(result[0].name, '01:00: Item1')

    def test_lookup_archive_item(self):
        uri = str(OE1LibraryUri(OE1UriType.ARCHIVE_ITEM,
                                '20140914', '1234567'))
        result = self.library.lookup(uri)
        self.client_mock.get_item.assert_called_once_with(
            '20140914', '1234567')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].uri, 'oe1:archive:20140914:1')
        self.assertEqual(result[0].name, '01:00: Item1')
