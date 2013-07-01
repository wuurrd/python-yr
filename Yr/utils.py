#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, json, datetime

class Location:
    """
    Internal class used to parse and find places and their api_url
    find returns the api_url used in the Yr-class.
    """
    def __init__(self, location, language):
        self.location = (location)
        self.language = (language)

    def find(self):
        import unicodecsv
        csv_file = (open('places_norway.csv', 'r'))
        data = (unicodecsv.reader(csv_file))
        matches = []
        for num, row in enumerate(data):
            if self.location in row[0]:
                matches.append(row)
        try:
            out = matches[0][3]
            if self.language is ('nb'):
                out = (matches[0][1])
            if self.language is ('nn'):
                out = (matches[0][2])
            if self.language is ('en'):
                out = (matches[0][3])
        except IndexError:
            pass
        if out is not None:
            return out.encode('utf-8')
        else:
            raise ValueError('Search got nothing')

class Connect:
    def __init__(self, location):
        self.location = (location)
        self.url = (self.location)

    def read(self):
        import urllib2 as urllib
        import xml.etree.cElementTree as et
        req = (urllib.Request(self.url, None, {'user-agent':'yr/wckd'}))
        opener = (urllib.build_opener())
        f = (opener.open(req).read())
        out = (et.fromstring(f))
        return out

class Cache:
    def __init__(self, location, cf):
        self.location = (location)
        self.cache_dir = ("/tmp/python-yr/")
        self.cache_file = (self.cache_dir+self.location+"."+cf)

        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def write(self, data):
        cf = open(self.cache_file, "w")
        cf.write(json.dumps(data))
        cf.close()

    def exists(self):
        if os.path.isfile(self.cache_file):
            return True
        else:
            return False

    def is_fresh(self):
        cf = open(self.cache_file).read()
        cfjs = json.loads(cf)
        timestamp = datetime.datetime.strptime(cfjs[0]['timestamp'], "%d.%m.%Y %H:%M:%S")
        out = False
        if datetime.datetime.now() - timestamp <= datetime.timedelta(minutes = 1):
            out = True
        return out

    def read(self):
        cf = open(self.cache_file).read()
        out = json.loads(cf)
        return out

    def remove(self):
        import errno
        try:
            os.remove(self.cache_file)
        except OSError, e:
            if e.errno != errno.ENOENT:
                raise
