from __future__ import unicode_literals

import unittest

from mopidy_oe1.client import OE1Client


class OE1ClientTest(unittest.TestCase):
    def test_get_days(self):
        oe1 = OE1Client(HttpClientMock())

        days = oe1.get_days()

        self.assertListEqual(days, [
            {'id': '20140913', 'label': 'Sa., 13.09.2014'},
            {'id': '20140914', 'label': 'So., 14.09.2014'}
        ])

    def test_get_day(self):
        oe1 = OE1Client(HttpClientMock())

        day = oe1.get_day('20140914')

        self.assertEqual(day, {'id': '20140914', 'label': 'So., 14.09.2014'})


class HttpClientMock(object):
    def __init__(self):
        self.urlMappings = {
            'http://oe1.orf.at/programm/konsole/heute': 'heute.json',
            'http://oe1.orf.at/programm/tag/20140913': 'tag20140913.json',
            'http://oe1.orf.at/programm/tag/20140914': 'tag20140914.json'
        }

    def get(self, url):
        file_name = 'tests/' + self.urlMappings[url]
        with open(file_name, 'r') as content_file:
            return content_file.read()
