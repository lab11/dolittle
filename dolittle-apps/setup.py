#!/usr/bin/env python

from distutils.core import setup

setup(name='Dolittle',
      version='1.0',
      description='MQTT-based stream processing platform',
      author='Meghan Clark',
      author_email='mclarkk@umich.edu',
      url='https://github.com/lab11/dolittle',
      packages=['phue', 'paho-mqtt', 'pattern'],
     )
