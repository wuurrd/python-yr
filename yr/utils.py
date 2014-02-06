#!/usr/bin/env python3

import os.path, sys, json, hashlib, requests, tempfile, datetime

class Language:

    def __init__(self, language):
        self.language = language

    def get_dictionary(self):
        filename = '../languages/{}.json'.format(self.language) # $$todo$$ ~> repair path!
        if os.path.exists(filename):
            with open(filename, mode='r') as f:
                return json.load(f)
        else:
            sys.stderr.write('error: unsupported language ~> {}\n'.format(self.language))
            sys.exit(1)

class Location:

    def __init__(self, location_name, language):
        self.location_name = location_name
        self.language = language
        self._ = Language(self.language).get_dictionary()
        self.url = self.get_url()
        self.hash = self.get_hash()

    def get_url(self):
        result = 'http://www.yr.no/{place}/{location_name}/{forecast}.xml'.format(location_name=self.location_name, **self._)
        return result

    def get_hash(self):
        result = hashlib.sha256(self.location_name.encode('utf-8')).hexdigest()[:12]
        return result

class Connect:

    def __init__(self, location):
        self.location = location

    def read(self):
        cache = Cache(self.location, 'forecast')
        if not cache.exists() or not cache.is_fresh():
            yr = requests.get(self.location.url)
            if not yr.status_code == requests.codes.ok:
                yr.raise_for_status()
            cache.write(yr.text)
        data = cache.read()
        return data

class Cache:

    cache_timeout = 30 # cache timeout in minutes

    def __init__(self, location, what):
        self.location = location
        self.cache_filename = '{}/{}.{}'.format(tempfile.gettempdir(), self.location.hash, what)

    def write(self, data):
        with open(self.cache_filename, mode='w') as f:
            f.write(data)

    def is_fresh(self):
        modified = datetime.datetime.fromtimestamp(os.path.getmtime(self.cache_filename))
        result = datetime.datetime.now() - modified <= datetime.timedelta(minutes=self.cache_timeout)
        return result

    def exists(self):
        result = os.path.isfile(self.cache_filename)
        return result

    def read(self):
        with open(self.cache_filename, mode='r') as f:
            data = f.read()
            return data
