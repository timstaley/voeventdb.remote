from voeventdb.remote.endpoints import apiv0 as apiv0_ep
from voeventdb.remote.keys import ResultKeys
import voeventdb.remote.request_wrappers as wrappers
import logging

logger = logging.getLogger(__name__)


def authored_month_count(filters=None,
                         host=None,
                         ):
    return wrappers.get_summary_data(endpoint=apiv0_ep.authored_month_count,
                            filters=filters,
                            host=host)


def count(filters=None,
          host=None,
          ):
    return wrappers.get_summary_data(endpoint=apiv0_ep.count,
                            filters=filters,
                            host=host)


def ivorn(filters=None,
          order=None,
          pagesize=None,
          n_max=None,
          host=None,
          ):
    return wrappers.get_list_data(list_endpoint=apiv0_ep.ivorn,
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
    return wrappers.get_list_data(list_endpoint=apiv0_ep.ivorn_cited_count,
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
    return wrappers.get_list_data(list_endpoint=apiv0_ep.ivorn_ref_count,
                         filters=filters,
                         order=order,
                         pagesize=pagesize,
                         n_max=n_max,
                         host=host,
                         )


def role_count(filters=None,
               host=None,
               ):
    return wrappers.get_summary_data(endpoint=apiv0_ep.role_count,
                            filters=filters,
                            host=host)


def stream_count(filters=None,
          host=None,
          ):
    return wrappers.get_summary_data(endpoint=apiv0_ep.stream_count,
                            filters=filters,
                            host=host)

def stream_role_count(filters=None,
          host=None,
          ):
    return wrappers.get_summary_data(endpoint=apiv0_ep.stream_role_count,
                            filters=filters,
                            host=host)

def synopsis(ivorn,
             host=None):
    r = wrappers.get_detail_response(endpoint=apiv0_ep.synopsis,
                            ivorn=ivorn,
                            host=host)
    return r.json()[ResultKeys.result]


def xml(ivorn,
        host=None):
    r = wrappers.get_detail_response(endpoint=apiv0_ep.xml_view,
                            ivorn=ivorn,
                            host=host)
    return r.text.encode('utf-8')
