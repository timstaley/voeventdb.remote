"""
Set up the package version, define some package-level variable defaults.
"""
from __future__ import absolute_import

from ._version import get_versions
__versiondict__ = get_versions()
__version__ = __versiondict__['version']
del get_versions

default_host = 'http://voeventdb.4pisky.org'
default_pagesize = 1000
default_list_n_max = 5000