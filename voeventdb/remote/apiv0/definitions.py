class Endpoints:
    root = "/apiv0/"
    authored_month_count = "/apiv0/authored_month_count"
    count = "/apiv0/count"
    ivorn = "/apiv0/ivorn"
    ivorn_cited_count = "/apiv0/ivorn_cited_count"
    ivorn_ref_count = "/apiv0/ivorn_ref_count"
    role_count = "/apiv0/role_count"
    stream_count = "/apiv0/stream_count"
    stream_role_count = "/apiv0/stream_role_count"
    synopsis = "/apiv0/synopsis/"
    xml_view = "/apiv0/xml/"

class FilterKeys:
    """
    Enumerates valid filters.

    Useful for building dictionaries representing filter-sets, eg.::

        filters = {
            FilterKeys.ivorn_contains: 'GRB',
            FilterKeys.role : 'observation',
        }

    For definitions of the various filters, and examples of valid
    values, see the :ref:`voeventdb query-filters <voeventdb:apiv0_filters>` page.

    """
    authored_since = 'authored_since'
    authored_until = 'authored_until'
    cited = 'cited'
    cone = 'cone'
    coord = 'coord'
    ivorn_contains = 'ivorn_contains'
    ivorn_prefix = 'ivorn_prefix'
    ref = 'ref'
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
    author_datetime_desc = 'author_datetime_desc'
    id = 'id'
    id_desc = 'id_desc'
    ivorn = 'ivorn'
    ivorn_desc = 'ivorn_desc'

class PaginationKeys:
    limit = 'limit'
    offset = 'offset'
    order = 'order'

class ResultKeys:
    endpoint = 'endpoint'
    limit = 'limit'
    querystring = 'querystring'
    result = 'result'
    url = 'url'

