from voeventdb.remote.definitions import ResultKeys
from voeventdb.remote.apiv1.definitions import Endpoints, FilterKeys
from voeventdb.remote.request_wrappers import (
    get_summary_data, get_list_data, get_detail_response
)
import logging
from voeventdb.remote.helpers import _map_citations

logger = logging.getLogger(__name__)


def map_authored_month_count(filters=None,
                             host=None,
                             ):
    return get_summary_data(endpoint=Endpoints.map_authored_month_count,
                            filters=filters,
                            host=host)

def _fetch_refs(ivorn):
    return [r['ref_ivorn'] for r in packet_synopsis(ivorn)['refs']]

def _fetch_cites(ref_ivorn):
    return list_ivorn({FilterKeys.ref_exact : ref_ivorn})

def citation_network_map(ivorn, max_recursion_levels=5):
    defaultdict_map =  _map_citations(
        ivorn=ivorn,
        fetch_refs_func=_fetch_refs,
        fetch_citations_func=_fetch_cites,
        max_recursion=max_recursion_levels
    )
    return dict(defaultdict_map)


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
