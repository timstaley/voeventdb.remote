#!/usr/bin/env python

from __future__ import print_function
from setuptools import setup, find_packages


install_requires = [
    'iso8601',
    'pytz',
    'requests',
    'simplejson',
    'astropy',
    'six',
]

test_requires = [
    'voeventdb[test]',
]

extras_require = {
    'test': test_requires,
    'all': test_requires,
}
packages = find_packages()
print("FOUND PACKAGES: ", packages)


setup(
    name="voeventdb.remote",
    version="0.1a0",
    description="Client-library for remotely querying the voeventdb REST API.",
    author="Tim Staley",
    author_email="timstaley337@gmail.com",
    url="https://github.com/timstaley/voeventdb.remote",
    packages=packages,
    install_requires=install_requires,
    extras_require=extras_require,
)
