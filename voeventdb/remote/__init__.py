"""
Define some package-level default values:
"""
from __future__ import absolute_import

from ._version import get_versions
__versiondict__ = get_versions()
__version__ = __versiondict__['version']
del get_versions

import voeventdb.remote.definitions

default_host = 'http://voeventdb.4pisky.org'
"""
The default host to query.
"""

default_list_n_max = 5000
"""
Maximum number of rows to fetch from a list request, by default.

If you really want to fetch more rows in a single query, this can be
changed for a single request by setting the ``n_max`` parameter-value.
Setting a value of ``n_max=0`` will fetch all available rows.
"""


default_pagesize = 1000
"""
Number of rows fetched in each HTTP GET request (when querying list-endpoints).

When many rows are available, the top-level interface will make
multiple GET requests behind the scenes, fetching `pagesize` rows
in each GET. This variable can typically be left unchanged
for casual usage - it's aimed at advanced usage when trying to improve
network performance.
"""


from . import _version
__version__ = _version.get_versions()['version']
