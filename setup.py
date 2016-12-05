#!/usr/bin/env python

from distutils.core import setup

setup(name='SeCupid',
      version='1.0',
      description='Selenium OkCupid',
      author='Stefan Safranek',
      author_email='sjsafranek@gmail.com',
      url='https://github.com/sjsafranek/secupid',
      packages=['selenium','secupid','SQLAlchemy'],
      package_dir={'secupid': 'secupid'},
     )
