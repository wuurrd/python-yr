#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, errno, json, datetime, hashlib
import xml.etree.cElementTree as et
import urllib2 as urllib
import unicodecsv

class Location:
    """
    Internal class used to parse and find places and their api_url
    find returns the api_url used in the Yr-class.
    """
    def __init__(self, location, language):
        self.location = (location)
        self.language = (language)

    def find(self):
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
        self.loc_hash = hashlib.sha256(self.location).hexdigest()

    def read(self):
        cache = Cache(self.loc_hash, "varsel")
        if cache.exists() and cache.is_fresh():
            #print "DEBUG: read saying cache exists"
            return (cache.read())
        else:
            #print "DEBUG: no cache"
            req = (urllib.Request(self.url, None, {'user-agent':'yr/wckd'}))
            opener = (urllib.build_opener())
            f = (opener.open(req).read())
            cache.write(f)
            return (cache.read())

class Cache:
    def __init__(self, location, cf):
        self.location = (location)
        self.cache_dir = ("/tmp/python-yr/")
        self.cache_file = (self.cache_dir+self.location+"."+cf)

        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def write(self, data):
        cf = open(self.cache_file, "w")
        #print "DEBUG: cache write"
        cf.write(data)
        cf.close()

    def is_fresh(self):
        modified = (os.path.getmtime(self.cache_file))
        out = False
        if datetime.datetime.now() - datetime.datetime.fromtimestamp(modified) <= datetime.timedelta(minutes = 10):
            out = True
        #print "DEBUG: cache is fresh:", out
        return out

    def exists(self):
        if os.path.isfile(self.cache_file):
            #print "DEBUG: cache exists"
            return True
        else:
            return False

    def read(self):
        cf = open(self.cache_file).read()
        #print "DEBUG: cache is read"
        return cf

    def remove(self):
        try:
            os.remove(self.cache_file)
        except OSError, e:
            if e.errno != errno.ENOENT:
                raise
