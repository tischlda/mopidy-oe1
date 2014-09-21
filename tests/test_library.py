from __future__ import unicode_literals

import unittest
import utils

from mopidy_oe1.library import OE1LibraryUri, OE1UriType, OE1LibraryProvider
from mopidy_oe1.client import OE1Client

class OE1LibraryUriTest(unittest.TestCase):
    def test_parse_root_uri(self):
        uri = 'oe1:directory'
        result = OE1LibraryUri.parse(uri)
        self.assertEqual(result.uri_type, OE1UriType.ROOT)

    def test_parse_live_uri(self):
        uri = 'oe1:live'
        result = OE1LibraryUri.parse(uri)
        self.assertEqual(result.uri_type, OE1UriType.LIVE)

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

    def test_create_archive_uri(self):
        parsed_uri = OE1LibraryUri(OE1UriType.ARCHIVE)
        self.assertEqual(str(parsed_uri), 'oe1:archive')

    def test_create_day_uri(self):
        parsed_uri = OE1LibraryUri(OE1UriType.ARCHIVE_DAY, '20140914')
        self.assertEqual(str(parsed_uri), 'oe1:archive:20140914')

    def test_create_item_uri(self):
        parsed_uri = OE1LibraryUri(OE1UriType.ARCHIVE_ITEM, '20140914', '382176')
        self.assertEqual(str(parsed_uri), 'oe1:archive:20140914:382176')