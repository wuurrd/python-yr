#!/usr/bin/env python3

import os, errno, datetime, hashlib, tempfile
import requests

class Location:
    def __init__(self, location, language):
        self.location = location
        self.language = language
        self.api_url = 'http://www.yr.no/'

    def find(self):
        if self.language is 'nb':
            place = 'sted/'
        elif self.language is 'nn':
            place = 'stad/'
        else:
            place = 'place/'
        yr_url = self.api_url + place+self.location + '/varsel.xml'
        return yr_url

class Connect:
    def __init__(self, location):
        self.url = location
        self.loc_hash = hashlib.sha256(self.url.encode('utf-8')).hexdigest()[:12]

    def read(self):
        cache = Cache(self.url, 'varsel')
        if cache.exists() and cache.is_fresh():
            return cache.read()
        yr = requests.get(self.url)
        if not yr.status_code == requests.codes.ok:
            yr.raise_for_status()
        f = yr.text
        cache.write(f)
        return cache.read()

class Cache:
    def __init__(self, location, cf):
        self.location = location
        self.loc_hash = hashlib.sha256(self.location.encode('utf-8')).hexdigest()[:12]
        self.temp_dir = tempfile.gettempdir() + '/'
        self.cache_file = self.temp_dir + self.loc_hash + '.' + cf

    def write(self, data):
        cf = open(self.cache_file, 'w')
        cf.write(data)
        cf.close()

    def is_fresh(self):
        modified = os.path.getmtime(self.cache_file)
        out = False
        if datetime.datetime.now() - datetime.datetime.fromtimestamp(modified) <= datetime.timedelta(minutes=10):
            out = True
        return out

    def exists(self):
        if os.path.isfile(self.cache_file):
            return True
        else:
            return False

    def read(self):
        cf = open(self.cache_file).read()
        return cf

    def remove(self):
        try:
            os.remove(self.cache_file)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise
