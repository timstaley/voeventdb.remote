from __future__ import absolute_import
default_host = 'http://voeventdb.4pisky.org'

default_pagesize = 1000

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
