#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, json, datetime

class Yr:
    def __init__(self, location, language):
        self.location = (location.decode('utf-8'))
        self.language = (language)
        self.now = datetime.datetime.now()

    def temperature(self):
        """
        Get temperature from yr and return it.
        """
        cache = Cache(self.location, "temperature")
        if cache.is_cached() and cache.is_fresh():
            return cache.read()
        else:
            location = (Location(self.location, self.language).find())
            data = (Connect(location).read())
            for temperature in data[5].iter('temperature'):
                if temperature.attrib:
                    out = {
                        'unit': temperature.attrib['unit'],
                        'value': temperature.attrib['value'],
                        'location': self.location,
                        'timestamp': self.now.strftime("%d.%m.%Y %H:%M:%S")
                    }
                    cache.create(out)
                    out = cache.read()
                    return out

    def wind_speed(self):
        """
        Get wind speed from yr.
        """
        cache = Cache(self.location, "wind_speed")
        if cache.is_cached() and cache.is_fresh():
            return cache.read()
        else:
            location = (Location(self.location, self.language).find())
            data = (Connect(location).read())
            for wind in data[5].iter('windSpeed'):
                if wind.attrib:
                    out = {
                        'location': self.location,
                        'mps': wind.attrib['mps'],
                        'unit': str('mps'),
                        'name': wind.attrib['name'],
                        'timestamp': self.now.strftime("%d.%m.%Y %H:%M:%S")
                    }
                    cache.create(out)
                    out = cache.read()
                    return out

    def wind_direction(self):
        """
        Get wind direction from yr.
        """
        cache = Cache(self.location, "wind_direction")
        if cache.is_cached() and cache.is_fresh():
            return cache.read()
        else:
            location = Location(self.location, self.language).find()
            data = Connect(location).read()
            for wind in data[5].iter('windDirection'):
                if wind.attrib:
                    out = {
                        'location': self.location,
                        'deg': wind.attrib['deg'],
                        'code': wind.attrib['code'],
                        'name': wind.attrib['name'],
                        'timestamp': self.now.strftime("%d.%m.%Y %H:%M:%S")
                    }
                    cache.create(out)
                    out = cache.read()
                    return out

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

    def create(self, data):
        cf = open(self.cache_file, "w")
        cf.write(json.dumps(data))
        cf.close()

    def is_cached(self):
        if os.path.isfile(self.cache_file):
            return True
        else:
            return False

    def is_fresh(self):
        cf = open(self.cache_file).read()
        cfjs = json.loads(cf)
        timestamp = datetime.datetime.strptime(cfjs['timestamp'], "%d.%m.%Y %H:%M:%S")
        out = False
        if datetime.datetime.now() - timestamp <= datetime.timedelta(minutes = 10):
            out = True
        return out

    def read(self):
        cf = open(self.cache_file).read()
        out = json.loads(cf)
        return out
