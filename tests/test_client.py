from __future__ import unicode_literals

import unittest

import utils

from mopidy_oe1.client import OE1Client


class OE1ClientTest(unittest.TestCase):
    def test_get_days(self):
        oe1 = OE1Client(utils.HttpClientMock())

        days = oe1.get_days()

        self.assertListEqual(days, [
            {'id': '20140913', 'label': 'Sa., 13.09.2014'},
            {'id': '20140914', 'label': 'So., 14.09.2014'}
        ])

    def test_get_day(self):
        oe1 = OE1Client(utils.HttpClientMock())

        day = oe1.get_day('20140914')

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
        oe1 = OE1Client(utils.HttpClientMock())

        day = oe1.get_item('20140914', '382176')

        self.assertEqual(day, {
            'id': '382176',
            'title': 'Nachrichten',
            'time': '06:00',
            'url': 'http://loopstream01.apa.at/?channel=oe1'
                   '&id=20140914_0600_1_2_nachrichten_XXX_w_'
        })
