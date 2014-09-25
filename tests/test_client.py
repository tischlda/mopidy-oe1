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
            {'id': '20140913', 'label': 'Sa., 13.09.2014'},
            {'id': '20140914', 'label': 'So., 14.09.2014'}
        ])

    def test_get_day(self):
        day = self.oe1_client.get_day('20140914')

        self.assertEqual(day, {
            'id': '20140914',
            'label': 'So., 14.09.2014',
            'items': [{
                'id': '382176',
                'title': 'Nachrichten',
                'time': '06:00',
                'url': 'http://loopstream01.apa.at/?channel=oe1'
                       '&id=20140914_0600_1_2_nachrichten_XXX_w_'
            }, {
                'id': '382177',
                'title': 'Guten Morgen \u00d6sterreich',
                'time': '06:05',
                'url': 'http://loopstream01.apa.at/?channel=oe1'
                       '&id=20140914_0605_4_1_gutenmorgenoesterreich_GMO_m_'
            }]
        })

    def test_get_item(self):
        day = self.oe1_client.get_item('20140914', '382176')

        self.assertEqual(day, {
            'id': '382176',
            'title': 'Nachrichten',
            'time': '06:00',
            'url': 'http://loopstream01.apa.at/?channel=oe1'
                   '&id=20140914_0600_1_2_nachrichten_XXX_w_'
        })
