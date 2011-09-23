#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools.core import setup
except ImportError:
    from distutils.core import setup

import os

install_requires = [
    'Django>=1.3',
]

setup(
    name = "django-agenda",
    version = "0.1",
    url = "http://github.com/fitoria/django-agenda",
    licence = 'MIT',
    description = 'Simple, pluggable and flexible agenda application for Django.',
    author = 'Adolfo Fitoria',
    author_email = 'adolfo.fitoria@gmail.com',
    install_requires = install_requires,
    packages = [],
    include_package_data = True,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Licence :: OSI Approved :: MIT Licence',
        'Programming Languaje :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
