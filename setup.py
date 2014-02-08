#!/usr/bin/env python3

from distutils.core import setup

setup(name='python-yr',
      version='1.2.1-dev',
      description='Get the forecast from the norwegian wheather service yr.no in python',
      author='Alexander Hansen, idxxx23 @ github',
      author_email='alexander.l.hansen@gmail.com',
      url='https://github.com/wckd/python-yr',
      packages=['yr'],
      install_requires=['requests', 'xmltodict', 'beautifulsoup4'],
     )
