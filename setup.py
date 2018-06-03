#!/usr/bin/env python
from setuptools import setup

setup(
    name='pvol',
    version='1.6',
    description='CLI PulseAudio volume control',
    author='Marcel Pietroń',
    author_email='mpietron@mail.com',
    install_requires=['pulsectl'],
    url='https://github.com/mrcl0/pvol',
    scripts=['pvol.py'],
    entry_points = {
              'console_scripts': [
                  'pvol = pvol:main',                  
              ],              
          },
)
