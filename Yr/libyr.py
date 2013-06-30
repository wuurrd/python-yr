#!/usr/bin/python
# -*- coding: utf-8 -*-
from utils import Cache, Connect, Location
import datetime

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
        if cache.exists() and cache.is_fresh():
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
                    cache.write(out)
                    out = cache.read()
                    return out

    def wind_speed(self):
        """
        Get wind speed from yr.
        """
        cache = Cache(self.location, "wind_speed")
        if cache.exists() and cache.is_fresh():
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
                    cache.write(out)
                    out = cache.read()
                    return out

    def wind_direction(self):
        """
        Get wind direction from yr.
        """
        cache = Cache(self.location, "wind_direction")
        if cache.exists() and cache.is_fresh():
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
                    cache.write(out)
                    out = cache.read()
                    return out
