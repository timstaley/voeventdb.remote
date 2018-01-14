from __future__ import print_function

import pytest

import voeventdb.remote.apiv1 as apiv1
from voeventdb.server.tests.fixtures.connection import simple_populated_db


def test_mock_requests_empty_db(mock_requests):
    count = apiv1.count()
    assert count == 0

def test_mock_requests_simpledb(mock_requests, simple_populated_db):
    dbinf = simple_populated_db
    count = apiv1.count()
    assert count == dbinf.n_inserts
