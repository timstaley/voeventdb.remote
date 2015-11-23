from contextlib import contextmanager
from six import string_types
import collections
import requests
import logging
logger = logging.getLogger(__name__)
from voeventdb.remote.keys import (
    ResultKeys as rkeys,
    PaginationKeys as pkeys
)

@contextmanager
def helpful_requests_error_log():
    """
    Provide 'ERROR' level log-messages pointing to common user-errors.

    Requests exceptions can be a bit cryptic for the uninitiated,
    so this context tries to give some helpful clues.

    """
    try:
        yield
    except requests.exceptions.ConnectionError:
        logger.error(
            "Could not establish connection, double-check your host address?")
        raise
    except requests.exceptions.MissingSchema:
        logger.error(
            "Could not establish connection - "
            "did you forget the 'http://' prefix when specifying the host?")
        raise
    finally:
        pass

def get_paginated(url, params, n_total, pagesize):
    offset = 0
    results = []
    localpars = params.copy()
    localpars[pkeys.limit] = pagesize
    while offset < n_total:
        localpars[pkeys.offset] = offset
        with helpful_requests_error_log():
            r = requests.get(url,
                             params=localpars
                             )
        r.raise_for_status()
        results.extend(r.json()[rkeys.result])
        offset += pagesize
    return results