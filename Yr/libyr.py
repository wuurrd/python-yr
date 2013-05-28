#!/usr/bin/python
# -*- coding: utf-8 -*-

class Yr:
    def __init__(self, location, language):
        self.location = (location.decode('utf-8'))
        self.language = (language)

    def temperature(self):
        """
        Get temperature from yr and return it.
        Returns a dict with 'location', 'value' and 'unit'.
        """
        try:
            location = Location(self.location, self.language).find()
            data = Connect(location).read()
        except AttributeError:
            pass
        try:
            for temperature in data[5].iter('temperature'):
                if temperature.attrib:
                    out = {
                        'unit': temperature.attrib['unit'], 
                        'value': temperature.attrib['value'], 
                        'location': self.location,
                    }
                    return out
                else:
                    return None
        except UnboundLocalError:
            return {'unit': None, 'value': None, 'location': None, }

    def wind_speed(self):
        """
        Get wind speed from yr.
        Returns a dict with 'location', 'unit', 'mps' and 'name'.
        """
        location = Location(self.location, self.language).find()
        data = Connect(location).read()

        for wind in data[5].iter('windSpeed'):
            if wind.attrib:
                out = {
                    'location': self.location,
                    'mps': wind.attrib['mps'],
                    'unit': str('mps'),
                    'name': wind.attrib['name'],
                }
                return out

    def wind_direction(self):
        """
        Get wind direction from yr.
        Returns a dict with 'location', 'deg', 'code' and 'name'.
        """
        location = Location(self.location, self.language).find()
        data = Connect(location).read()

        for wind in data[5].iter('windDirection'):
            if wind.attrib:
                out = {
                    'location': self.location,
                    'deg': wind.attrib['deg'],
                    'code': wind.attrib['code'],
                    'name': wind.attrib['name'],
                }
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
        csv_file = open('places_norway.csv', 'r')
        data = unicodecsv.reader(csv_file)
        matches = []
        for num, row in enumerate(data):
            if self.location in row[0]:
                matches.append(row)
        out = None
        try:
            out = matches[0][3]
            if self.language is ('nb'):
                out = matches[0][1]
            if self.language is ('nn'):
                out = matches[0][2]
            if self.language is ('en'):
                out = matches[0][3]
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
        if self.url is None:
            raise ValueError('No url found')
        import urllib2 as urllib
        import xml.etree.cElementTree as et
        req = urllib.Request(self.url, None, {'user-agent':'yr/wckd'})
        opener = (urllib.build_opener())
        f = (opener.open(req))
        r = (f.read())
        out = et.fromstring(r)
        return out
