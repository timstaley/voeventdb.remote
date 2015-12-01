from __future__ import print_function
import pytest
from voeventdb.server.tests.fixtures.connection import simple_populated_db

import voeventdb.remote as vr

def test_mock_requests_empty_db(mock_requests):
    count = vr.count()
    assert count == 0

def test_mock_requests_simpledb(mock_requests, simple_populated_db):
    dbinf = simple_populated_db
    count = vr.count()
    assert count == dbinf.n_inserts