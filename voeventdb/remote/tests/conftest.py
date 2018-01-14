from __future__ import print_function

import logging

import flask
import pytest
import requests

import voeventdb.remote as vr
from voeventdb.server.restapi.app import app
from voeventdb.server.tests.fixtures.connection import (
    empty_db_connection,
    fixture_db_session,
    simple_populated_db,
)

logger = logging.getLogger('vdbr-tests')


@pytest.fixture
def mock_requests(fixture_db_session):
    # print
    # print "setting up flask client"
    app.testing = True
    client = app.test_client()
    app_context = app.test_request_context()
    app_context.push()

    def mock_requests_get(url, params=None, **kwargs):
        """
        A mocked version of requests.get, fetches using the flask test client.

        This is pretty ugly, but I think it makes sense now:
        We 'prepare' the request, which takes the 'params' and builds them
        into the url. We can extract the url minus the 'host' prefix as
        ``prepped.path_url``, which is fortunately exactly what the flask
        ``test_client.get()`` method needs as an argument.

        Now, we want all the usual requests.Response behaviours, so we
        manually initialise one and assign ``._content`` as the data returned
        from our flask test-client.
        """
        # print("USING MOCKED GET FUNCTION")
        req = requests.Request('GET', url, params=params, **kwargs)
        prepped = req.prepare()
        full_url = prepped.url
        # print("PATH URL", prepped.path_url)
        logger.debug("Fetching {}".format(prepped.path_url))
        flask_response = client.get(prepped.path_url)
        req_resp = requests.Response()
        req_resp._content = flask_response.data
        req_resp.status_code = flask_response.status_code
        return req_resp

    original_get = requests.get
    requests.get = mock_requests_get
    yield
    app_context.pop()
    del app_context
    requests.get = original_get


@pytest.fixture
def reset_globals_to_defaults():
    host = vr.default_host
    list_max = vr.default_list_n_max
    pagesize = vr.default_pagesize
    yield
    vr.default_host = host
    vr.default_list_n_max = list_max
    vr.default_pagesize = pagesize
