#!/usr/bin/python
# -*- coding: utf-8 -*-

class place2url:
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
        if self.language is ("nb"):
            matches = matches[0][1]
        if self.language is ("nn"):
            matches = matches[0][2]
        if self.language is ("en"):
            matches = matches[0][3]
        return matches

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

class Yr:
    def __init__(self, location, language):
        self.location = (location)
        self.language = (language)

    def get_temperature(self):
        """
        Get temperature from yr and return it.
        Returns a dict with 'value' and 'unit'.
        """
        location = place2url(self.location, self.language).find()
        location = location.encode("utf-8")
        get = Connect(location).read()
        for temperature in get[5].iter('temperature'):
            return temperature.attrib
