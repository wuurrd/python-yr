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
            out = []
            for temperature in data[5].iter('temperature'):
                if temperature.attrib:
                    out.append({
                        'unit': temperature.attrib['unit'],
                        'value': temperature.attrib['value'],
                        'location': self.location,
                        'timestamp': self.now.strftime("%d.%m.%Y %H:%M:%S"),
                    })
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
            out = []
            for wind in data[5].iter('windSpeed'):
                if wind.attrib:
                    out.append({
                        'location': self.location,
                        'mps': wind.attrib['mps'],
                        'unit': str('mps'),
                        'name': wind.attrib['name'],
                        'timestamp': self.now.strftime("%d.%m.%Y %H:%M:%S"),
                    })
                    cache.write(out)
                    return cache.read()

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
            out = []
            for wind in data[5].iter('windDirection'):
                if wind.attrib:
                    out.append({
                        'location': self.location,
                        'deg': wind.attrib['deg'],
                        'code': wind.attrib['code'],
                        'name': wind.attrib['name'],
                        'timestamp': self.now.strftime("%d.%m.%Y %H:%M:%S"),
                    })
                    cache.write(out)
                    return cache.read()

    def forecast(self):
        cache = Cache(self.location, "forecast")
        if cache.exists() and cache.is_fresh():
            return cache.read()
        else:
            location = Location(self.location, self.language).find()
            data = Connect(location).read()
            days = []
            for items in data[5][0].iter('text'):
                for child in items[0]:
                    days.append({
                        'from': child.get('from'), 
                        'to': child.get('to'), 
                        child[0].tag: child[0].text, 
                        child[1].tag: child[1].text,
                        'location': self.location,
                        'timestamp': self.now.strftime("%d.%m.%Y %H:%M:%S"),
                      })
                cache.write(days)
                return cache.read()
