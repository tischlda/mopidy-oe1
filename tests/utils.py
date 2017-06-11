from __future__ import unicode_literals


class HttpClientMock(object):
    def __init__(self):
        self.urlMappings = {
            'http://audioapi.orf.at/oe1/json/2.0/broadcasts/':
                'broadcasts.json',
            'https://audioapi.orf.at/oe1/api/json/current/broadcast/475617':
                'broadcast475617.json'
        }

    def get(self, url):
        file_name = self.urlMappings[url]
        with open(file_name, 'r') as content_file:
            return content_file.read()
