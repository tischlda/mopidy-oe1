from __future__ import unicode_literals

import logging

from mopidy import backend

import pykka
from mopidy_oe1.library import OE1LibraryProvider

logger = logging.getLogger(__name__)

class OE1PlaybackProvider(backend.PlaybackProvider):
    def change_track(self, track):
        track = track.copy(uri='http://loopstream01.apa.at/?channel=oe1&id=20140914_0700_1_3_nachrichten_XXX_w_')
        return super(OE1PlaybackProvider, self).change_track(track)