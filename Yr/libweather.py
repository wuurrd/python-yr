#!/usr/bin/python
import urllib2 as urllib

api_url = ("http://www.yr.no/sted/")

class Connect:
    def __init__(self, location):
        self.location = (location)
        self.url = (api_url+"%s") % (self.location)

    def read(self):
        import xml.etree.cElementTree as et
        req = urllib.Request(self.url, None, {'user-agent':'yr/wckd'})
        opener = (urllib.build_opener())
        f = (opener.open(req))
        read = (f.read())
        out = et.fromstring(read)
        return out

class Yr:
    def __init__(self, location):
        self.location = (location)

    def return_place(self):
        return(self.location)

    def get_temperature(self):
        location = (self.location+"/forecast.xml")
        get = Connect(location).read()
        for temperature in get[5].iter('temperature'):
            return temperature.attrib
        return forecast
