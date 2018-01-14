"""
Functions representing endpoints

Endpoint definitions can be found in the
:ref:`server-docs <voeventdbserver:apiv1_endpoints>`.
Function calls use a consistent style throughout:

- For all endpoints you can specify a particular ``host``. If this is ``None``,
  the  :attr:`default host <voeventdb.remote.default_host>` will be used.
- All endpoint-functions can be passed ``filters``,
  a dictionary defining a set of
  :class:`filter-keys <.FilterKeys>` and
  values
  (except for the `packet_` functions,
  which retrieve details on a single packet as specified by the IVORN).
- `List` endpoints can be passed an ``order``
  (see :class:`.OrderValues`),
  and an ``n_max`` parameter which
  limits the number of list-items returned.
  There is also a ``pagesize``
  parameter, but this can typically be left at the default setting
  (see :attr:`voeventdb.remote.default_pagesize`).



.. note::

    These are imported into the ``apiv1`` namespace for brevity, so you can
    access them like ``voeventdb.remote.apiv1.count()``.
"""
# (Actually just convenient partial-bindings to request_wrappers).

import logging

from voeventdb.remote.apiv1.definitions import Endpoints, FilterKeys
from voeventdb.remote.definitions import ResultKeys
from voeventdb.remote.request_wrappers import (
    get_detail_response,
    get_list_data,
    get_summary_data,
)

logger = logging.getLogger(__name__)


def count(filters=None,
          host=None,
          ):
    return get_summary_data(endpoint=Endpoints.count,
                            filters=filters,
                            host=host)


def list_ivorn(filters=None,
               order=None,
               pagesize=None,
               n_max=None,
               host=None,
               ):
    return get_list_data(list_endpoint=Endpoints.list_ivorn,
                         count_endpoint=Endpoints.count,
                         filters=filters,
                         order=order,
                         pagesize=pagesize,
                         n_max=n_max,
                         host=host,
                         )


def list_ivorn_ncites(filters=None,
                      order=None,
                      pagesize=None,
                      n_max=None,
                      host=None,
                      ):
    return get_list_data(list_endpoint=Endpoints.list_ivorn_ncites,
                         count_endpoint=Endpoints.count,
                         filters=filters,
                         order=order,
                         pagesize=pagesize,
                         n_max=n_max,
                         host=host,
                         )


def list_ivorn_nrefs(filters=None,
                     order=None,
                     pagesize=None,
                     n_max=None,
                     host=None,
                     ):
    return get_list_data(list_endpoint=Endpoints.list_ivorn_nrefs,
                         count_endpoint=Endpoints.count,
                         filters=filters,
                         order=order,
                         pagesize=pagesize,
                         n_max=n_max,
                         host=host,
                         )

def map_authored_month_count(filters=None,
                             host=None,
                             ):
    return get_summary_data(endpoint=Endpoints.map_authored_month_count,
                            filters=filters,
                            host=host)

def map_role_count(filters=None,
                   host=None,
                   ):
    return get_summary_data(endpoint=Endpoints.map_role_count,
                            filters=filters,
                            host=host)


def map_stream_count(filters=None,
                     host=None,
                     ):
    return get_summary_data(endpoint=Endpoints.map_stream_count,
                            filters=filters,
                            host=host)


def map_stream_role_count(filters=None,
                          host=None,
                          ):
    return get_summary_data(endpoint=Endpoints.map_stream_role_count,
                            filters=filters,
                            host=host)


def packet_synopsis(ivorn,
                    host=None):
    r = get_detail_response(endpoint=Endpoints.packet_synopsis,
                            ivorn=ivorn,
                            host=host)
    return r.json()[ResultKeys.result]


def packet_xml(ivorn,
               host=None):
    r = get_detail_response(endpoint=Endpoints.packet_xml,
                            ivorn=ivorn,
                            host=host)
    return r.text.encode('utf-8')
