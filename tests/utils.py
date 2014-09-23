from __future__ import unicode_literals


class HttpClientMock(object):
    def __init__(self):
        self.urlMappings = {
            'http://oe1.orf.at/programm/konsole/heute':
                'heute.json',
            'http://oe1.orf.at/programm/konsole/tag/20140913':
                'tag20140913.json',
            'http://oe1.orf.at/programm/konsole/tag/20140914':
                'tag20140914.json'
        }

    def get(self, url):
        file_name = 'tests/' + self.urlMappings[url]
        with open(file_name, 'r') as content_file:
            return content_file.read()
