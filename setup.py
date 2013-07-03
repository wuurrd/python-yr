#!/usr/bin/env python

from distutils.core import setup

setup(name='python-yr',
      version='1.0-dev',
      description='Get the forecast from the norwegian wheather service yr.no in python',
      author='Alexander Hansen',
      author_email='alexander.l.hansen@gmail.com',
      url='https://github.com/wckd/python-yr',
      packages=['yr'],
      package_data = {'yr': ['data/*.csv'] },
      include_package_data=True,
      install_requires=['unicodecsv'],
     )
