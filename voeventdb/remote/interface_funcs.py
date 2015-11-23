import urllib
import requests
import requests.exceptions
import voeventdb.remote.endpoints
from voeventdb.remote.endpoints import apiv0
from voeventdb.remote.keys import (
    PaginationKeys as pkeys,
    ResultKeys as rkeys,
)
from voeventdb.remote.utils import (
    helpful_requests_error_log,
    get_paginated
)
import voeventdb.remote

import logging

logger = logging.getLogger(__name__)


def count_matching(filters=None,
                   host=None,
                   ):
    if host is None:
        host = voeventdb.remote.default_host
    params = filters
    with helpful_requests_error_log():
        r = requests.get(host + apiv0.count,
                         params=params
                         )
    r.raise_for_status()
    return r.json()[rkeys.result]


def get_synopsis(ivorn,
                 host=None):
    if host is None:
        host = voeventdb.remote.default_host
    ep_url = host + apiv0.synopsis
    url = ep_url + urllib.quote_plus(ivorn)
    with helpful_requests_error_log():
        r = requests.get(url)
    r.raise_for_status()
    return r.json()[rkeys.result]


def get_xml(ivorn,
            host=None):
    if host is None:
        host = voeventdb.remote.default_host
    ep_url = host + apiv0.xml_view
    url = ep_url + urllib.quote_plus(ivorn)
    with helpful_requests_error_log():
        r = requests.get(url)
    r.raise_for_status()
    return r.text.encode('utf-8')


def list_ivorns(filters=None,
                pagesize=None,
                host=None,
                ):
    if host is None:
        host = voeventdb.remote.default_host
    if pagesize is None:
        pagesize = voeventdb.remote.default_pagesize
    params = filters

    n_matched = count_matching(filters, host)

    params[pkeys.limit] = n_matched

    results = get_paginated(url=host + apiv0.ivorn,
                            params=params,
                            n_total=n_matched,
                            pagesize=pagesize,
                            )

    return results
