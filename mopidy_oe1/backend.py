from __future__ import unicode_literals

import logging

from mopidy import backend

import pykka
from mopidy_oe1.library import OE1LibraryProvider

logger = logging.getLogger(__name__)

class OE1Backend(pykka.ThreadingActor, backend.Backend):
    def __init__(self, config, audio):
        super(OE1Backend, self).__init__()

        self.config = config

        self.library = OE1LibraryProvider(backend = self)

        self.uri_schemes = ['oe1']

    def on_start(self):
        logger.info('Starting OE1Backend')

    def on_stop(self):
        pass
