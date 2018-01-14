import logging
from contextlib import contextmanager

import requests

logger = logging.getLogger(__name__)

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
