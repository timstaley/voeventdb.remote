"""
Classes enumerated things specific to apiv1.

These are intended to be useful to the end-user in building queries.
"""

class Endpoints:
    ## Regex from server inspection output:
    ## ^'(.*)': (.*').* -> $1 = $2
    ## Then:
    ## ([\w]*)/(.*) -> $1_$2
    root = '/apiv1/'
    count = '/apiv1/count'
    list_ivorn = '/apiv1/list/ivorn'
    list_ivorn_ncites = '/apiv1/list/ivorn_ncites'
    list_ivorn_nrefs = '/apiv1/list/ivorn_nrefs'
    map_authored_month_count = '/apiv1/map/authored_month_count'
    map_role_count = '/apiv1/map/role_count'
    map_stream_count = '/apiv1/map/stream_count'
    map_stream_role_count = '/apiv1/map/stream_role_count'
    packet_synopsis = '/apiv1/packet/synopsis/'
    packet_xml = '/apiv1/packet/xml/'


class FilterKeys:
    """
    Enumerates valid filters.

    Useful for building dictionaries representing filter-sets, eg.::

        filters = {
            FilterKeys.ivorn_contains: 'GRB',
            FilterKeys.role : 'observation',
        }

    For definitions of the various filters, and examples of valid
    values, see the :ref:`voeventdb query-filters <voeventdb:apiv1_filters>` page.

    """
    authored_since = 'authored_since'
    authored_until = 'authored_until'
    cited = 'cited'
    cone = 'cone'
    coord = 'coord'
    dec_greater_than = 'dec_gt'
    dec_less_than = 'dec_lt'
    ivorn_contains = 'ivorn_contains'
    ivorn_prefix = 'ivorn_prefix'
    ref_any = 'ref_any'
    ref_contains = 'ref_contains'
    ref_exact = 'ref_exact'
    role = 'role'
    stream = 'stream'

class OrderValues:
    """
    Enumerates valid orderings.

    For details see :ref:`this section <voeventdb:ordervalues>` in
    the *voeventdb.server* docs.

    """
    author_datetime = 'author_datetime'
    author_datetime_desc = '-author_datetime'
    id = 'id'
    id_desc = '-id'
    ivorn = 'ivorn'
    ivorn_desc = '-ivorn'



