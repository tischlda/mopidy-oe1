from __future__ import unicode_literals

import unittest

import utils

from mopidy_oe1.client import OE1Client


class OE1ClientTest(unittest.TestCase):
    def setUp(self):
        self.http_client_mock = utils.HttpClientMock()
        self.oe1_client = OE1Client(self.http_client_mock)

    def test_get_days(self):
        days = self.oe1_client.get_days()

        self.assertListEqual(days, [
            {'id': '20170605', 'label': 'Mon 05. Jun 2017'},
            {'id': '20170604', 'label': 'Sun 04. Jun 2017'}
        ])

    def test_get_day(self):
        day = self.oe1_client.get_day('20170604')

        self.assertEqual(day, {
            'id': '20170604',
            'label': 'Sun 04. Jun 2017',
            'items': [{
                'id': '0',
                'title': 'Nachrichten',
                'time': '10:59:49'
            }, {
                'id': '1',
                'title': 'Matinee',
                'time': '11:02:57'
            }]
        })

    def test_get_item(self):
        day = self.oe1_client.get_item('20170604', '0')

        self.assertEqual(day, {
            'id': '0',
            'title': 'Nachrichten',
            'time': '10:59:49'
        })
