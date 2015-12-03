from __future__ import absolute_import
default_host = 'http://voeventdb.4pisky.org'

default_pagesize = 1000

from ._version import get_versions
__versiondict__ = get_versions()
__version__ = __versiondict__['version']
del get_versions
