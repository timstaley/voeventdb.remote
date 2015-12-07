"""
Define some package-level default values:
"""
from __future__ import absolute_import

from ._version import get_versions
__versiondict__ = get_versions()
__version__ = __versiondict__['version']
del get_versions

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

Note that if more rows are available, multiple GET requests are
made 'behind the scenes' when using the top-level interface,
so this variable can typically be left unchanged
for casual usage - it's aimed at advanced usage when trying to improve
performance with large queries.
"""

