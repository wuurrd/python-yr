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
            api_url = location.encode('utf-8')
            data = Connect(api_url).read()
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
        api_url = location.encode('utf-8')
        data = Connect(api_url).read()

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
        Returns a dict with 'deg', 'code' and 'name'.
        """
        pass

    def forecast(self):
        """
        Get the forecast from yr.
        """
        pass

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
        csvlist = []
        for row in data:
            if data.line_num:
                csvlist.append(row)
        matches = [x for x in csvlist if self.location in x]
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
            #TODO: Legg inn oppslag her om ingenting blir funnet i csv
            pass
        return out

class Connect:
    def __init__(self, location):
        self.location = (location)
        self.url = (self.location)

    def read(self):
        import urllib2 as urllib
        import xml.etree.cElementTree as et
        req = urllib.Request(self.url, None, {'user-agent':'yr/wckd'})
        opener = (urllib.build_opener())
        f = (opener.open(req))
        r = (f.read())
        out = et.fromstring(r)
        return out
