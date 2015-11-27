import urllib
import voeventdb.remote.endpoints
from voeventdb.remote.endpoints import apiv0
from voeventdb.remote.keys import ResultKeys
from voeventdb.remote.request_wrappers import (
    get_summary_data,
    get_detail_response,
    get_list_data,
)
import logging

logger = logging.getLogger(__name__)


def count(filters=None,
          host=None,
          ):
    return get_summary_data(endpoint=apiv0.count,
                            filters=filters,
                            host=host)


def ivorn(filters=None,
          order=None,
          pagesize=None,
          n_max=None,
          host=None,
          ):
    return get_list_data(list_endpoint=apiv0.ivorn,
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
    return get_list_data(list_endpoint=apiv0.ivorn_cited_count,
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
    return get_list_data(list_endpoint=apiv0.ivorn_ref_count,
                         filters=filters,
                         order=order,
                         pagesize=pagesize,
                         n_max=n_max,
                         host=host,
                         )


def synopsis(ivorn,
             host=None):
    r = get_detail_response(endpoint=apiv0.synopsis,
                            ivorn=ivorn,
                            host=host)
    return r.json()[ResultKeys.result]


def xml(ivorn,
        host=None):
    r = get_detail_response(endpoint=apiv0.xml_view,
                            ivorn=ivorn,
                            host=host)
    return r.text.encode('utf-8')
