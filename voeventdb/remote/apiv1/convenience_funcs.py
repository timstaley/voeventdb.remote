from voeventdb.remote.definitions import ResultKeys
from voeventdb.remote.apiv1.definitions import Endpoints, FilterKeys
from voeventdb.remote.request_wrappers import (
    get_summary_data, get_list_data, get_detail_response
)
import logging
from voeventdb.remote.helpers import _map_citations

logger = logging.getLogger(__name__)


def authored_month_count(filters=None,
                         host=None,
                         ):
    return get_summary_data(endpoint=Endpoints.authored_month_count,
                            filters=filters,
                            host=host)

def _fetch_refs(ivorn):
    return [ r['ref_ivorn'] for r in synopsis(ivorn)['refs']]

def _fetch_cites(ref_ivorn):
    return ivorn({FilterKeys.ref_exact : ref_ivorn})

def citation_network_map(ivorn, max_recursion_levels=5):
    return _map_citations(
        ivorn=ivorn,
        fetch_refs_func=_fetch_refs,
        fetch_citations_func=_fetch_cites,
        max_recursion=max_recursion_levels
    )


def count(filters=None,
          host=None,
          ):
    return get_summary_data(endpoint=Endpoints.count,
                            filters=filters,
                            host=host)


def ivorn(filters=None,
          order=None,
          pagesize=None,
          n_max=None,
          host=None,
          ):
    return get_list_data(list_endpoint=Endpoints.ivorn,
                         count_endpoint=Endpoints.count,
                         filters=filters,
                         order=order,
                         pagesize=pagesize,
                         n_max=n_max,
                         host=host,
                         )


def ivorn_cited_count(filters=None,
                      order=None,
                      pagesize=None,
                      n_max=None,
                      host=None,
                      ):
    return get_list_data(list_endpoint=Endpoints.ivorn_cited_count,
                         count_endpoint=Endpoints.count,
                         filters=filters,
                         order=order,
                         pagesize=pagesize,
                         n_max=n_max,
                         host=host,
                         )


def ivorn_ref_count(filters=None,
                    order=None,
                    pagesize=None,
                    n_max=None,
                    host=None,
                    ):
    return get_list_data(list_endpoint=Endpoints.ivorn_ref_count,
                         count_endpoint=Endpoints.count,
                         filters=filters,
                         order=order,
                         pagesize=pagesize,
                         n_max=n_max,
                         host=host,
                         )


def role_count(filters=None,
               host=None,
               ):
    return get_summary_data(endpoint=Endpoints.role_count,
                            filters=filters,
                            host=host)


def stream_count(filters=None,
                 host=None,
                 ):
    return get_summary_data(endpoint=Endpoints.stream_count,
                            filters=filters,
                            host=host)


def stream_role_count(filters=None,
                      host=None,
                      ):
    return get_summary_data(endpoint=Endpoints.stream_role_count,
                            filters=filters,
                            host=host)


def synopsis(ivorn,
             host=None):
    r = get_detail_response(endpoint=Endpoints.synopsis,
                            ivorn=ivorn,
                            host=host)
    return r.json()[ResultKeys.result]


def xml(ivorn,
        host=None):
    r = get_detail_response(endpoint=Endpoints.xml_view,
                            ivorn=ivorn,
                            host=host)
    return r.text.encode('utf-8')
