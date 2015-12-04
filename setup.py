#!/usr/bin/env python

from __future__ import print_function
from setuptools import setup, find_packages
import versioneer


install_requires = [
    'iso8601',
    'pytz',
    'requests',
    'simplejson',
    'astropy',
    'six',
]

test_requires = [
    'voeventdb.server[test]',
]

extras_require = {
    'test': test_requires,
    'all': test_requires,
}
packages = find_packages()
print("FOUND PACKAGES: ", packages)


setup(
    name="voeventdb.remote",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Client-library for remotely querying the voeventdb REST API.",
    author="Tim Staley",
    author_email="timstaley337@gmail.com",
    url="https://github.com/timstaley/voeventdb.remote",
    packages=packages,
    install_requires=install_requires,
    extras_require=extras_require,
)
