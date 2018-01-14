import datetime
import json
import logging
import urllib

import requests
import requests.exceptions
import six
from astropy.coordinates import Angle, SkyCoord
from six import string_types

import voeventdb.remote
from voeventdb.remote.definitions import PaginationKeys, ResultKeys
from voeventdb.remote.utils import helpful_requests_error_log

if six.PY3:
    from urllib.parse import quote_plus
else:
    from urllib import quote_plus

logger = logging.getLogger(__name__)


def format_conesearch_params(input):
    """
    Validates and formats parameters for the cone-search filter.
    """
    if not input:
        raise ValueError(
            "Cannot format {} to valid cone-search params".format(input))

    try:
        if isinstance(input, string_types):
            # Assume preformatted (ra,dec,err) json-list:
            try:
                ra, dec, err = json.loads(input)
            except json.JSONDecodeError as e:
                logger.error('Unable to parse input "{}" as JSON'.format(input))
                raise ValueError
            posn = SkyCoord(ra, dec, unit='deg')
            posn_error = Angle(err, unit='deg')
        elif len(input) == 2:
            # Assume (Skycoord, Angle) tuple:
            posn = SkyCoord(input[0])
            posn_error = Angle(input[1])
        elif len(input) == 3:
            # Assume simple (ra,dec,err) tuple:
            # We still parse via SkyCoord, this provides validation.
            posn = SkyCoord(input[0], input[1], unit='deg')
            posn_error = Angle(input[2], unit='deg')
        else:
            raise TypeError
    except:
        logger.error(
            'Cannot parse or convert "{}" as valid SkyCoord / Angle '
            'for cone-search '.format(input))
        raise
    return str([posn.ra.deg, posn.dec.deg, posn_error.deg])


def format_filters(filters):
    """
    Perform any necessary autoconversion of filter-values to strings.

    For example, we isoformat any datetimes.
    """
    if not filters:
        return filters
    formatted = {}
    for k, v in filters.items():
        if isinstance(v, datetime.datetime):
            formatted[k] = v.isoformat()
        else:
            formatted[k] = v
    if 'cone' in filters:
        formatted['cone'] = format_conesearch_params(filters['cone'])
    return formatted


def get_summary_response(endpoint,
                         filters,
                         host,
                         ):
    if host is None:
        host = voeventdb.remote.default_host
    params = format_filters(filters)
    with helpful_requests_error_log():
        r = requests.get(host + endpoint,
                         params=params
                         )
    r.raise_for_status()
    return r


def get_summary_data(endpoint,
                     filters,
                     host,
                     ):
    r = get_summary_response(endpoint, filters, host)
    return r.json()[ResultKeys.result]


def get_detail_response(endpoint,
                        ivorn,
                        host):
    if host is None:
        host = voeventdb.remote.default_host
    ep_url = host + endpoint
    url = ep_url + quote_plus(ivorn)
    with helpful_requests_error_log():
        r = requests.get(url)
    r.raise_for_status()
    return r


def get_paginated(url, params, n_to_fetch, pagesize):
    offset = 0
    results = []
    localpars = params.copy()
    localpars[PaginationKeys.limit] = pagesize
    if n_to_fetch < pagesize:
        localpars[PaginationKeys.limit] = n_to_fetch
    while offset < n_to_fetch:
        localpars[PaginationKeys.offset] = offset
        with helpful_requests_error_log():
            r = requests.get(url,
                             params=localpars
                             )
        r.raise_for_status()
        results.extend(r.json()[ResultKeys.result])
        offset += pagesize
    # Snip any excess results caused by n_to_fetch not being
    # a multiple of pagesize
    results = results[:n_to_fetch]
    return results


def get_list_data(list_endpoint,
                  count_endpoint,
                  filters=None,
                  order=None,
                  n_max=None,
                  pagesize=None,
                  host=None,
                  ):
    if host is None:
        host = voeventdb.remote.default_host
    if pagesize is None:
        pagesize = voeventdb.remote.default_pagesize
    params = {}
    if filters:
        params.update(format_filters(filters))

    n_matched = get_summary_data(endpoint=count_endpoint,
                                 filters=filters,
                                 host=host)
    if n_max is None:
        n_max = voeventdb.remote.default_list_n_max
    if n_max:
        n_to_fetch = min(n_matched, n_max)
    else:
        n_to_fetch = n_matched

    if order:
        params[PaginationKeys.order] = order

    results = get_paginated(url=host + list_endpoint,
                            params=params,
                            n_to_fetch=n_to_fetch,
                            pagesize=pagesize,
                            )

    return results
