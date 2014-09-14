from __future__ import unicode_literals

import logging

from mopidy import backend
from mopidy.models import Ref, Track

logger = logging.getLogger(__name__)

class OE1LibraryProvider(backend.LibraryProvider):
    root_directory = Ref.directory(uri='oe1:directory', name='OE1')

    def __init__(self, *args, **kwargs):
        super(OE1LibraryProvider, self).__init__(*args, **kwargs)

        self._root = [
            Ref.directory(uri='oe1:live', name='Live'),
            Ref.directory(uri='oe1:archive', name='7 Tage')]

    def browse(self, uri):
        if(uri == self.root_directory.uri):
            return self._root

    def find_exact(self, query=None, uris=None):
        return []

    def lookup(self, uri):
        return []

    def refresh(self, uri=None):
        pass

    def search(self, query=None, uris=None):
        return []