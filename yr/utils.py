#!/usr/bin/env python3

import os.path, sys, json, hashlib, requests, tempfile, datetime
#import errno

def hash(what):
    result = hashlib.sha256(what.encode('utf-8')).hexdigest()[:12]
    return result

class Location:

    def __init__(self, location, language):
        self.location = location
        self.language = language
        filename = '../languages/{}.json'.format(language) # $$todo$$ ~> repair path!
        if os.path.exists(filename):
            with open(filename, mode='r') as f:
                self._ = json.load(f)
        else:
            sys.stderr.write('error: unsupported language ~> {}\n'.format(language))
            sys.exit(1)

    def find(self):
        result = 'http://www.yr.no/{place}/{location}/{forecast}.xml'.format(location=self.location, **self._)
        return result

class Connect:

    def __init__(self, location):
        self.location = location
        self.loc_hash = hash(location)

    def read(self):
        cache = Cache(self.location, 'forecast')
        if not cache.exists() or not cache.is_fresh():
            yr = requests.get(self.location)
            if not yr.status_code == requests.codes.ok:
                yr.raise_for_status()
            cache.write(yr.text)
        data = cache.read()
        return data

class Cache:

    cache_timeout = 30 # cache timeout in minutes

    def __init__(self, location, what):
        self.location = location
        self.loc_hash = hash(location)
        self.cache_filename = '{}/{}.{}'.format(tempfile.gettempdir(), self.loc_hash, what)

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

    '''
    def remove(self):
        try:
            os.remove(self.cache_filename)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise
    '''
