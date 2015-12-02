from __future__ import print_function
import pytest
import voeventdb.remote as vr
import voeventdb.remote.request_wrappers as wrappers
from voeventdb.remote.endpoints import apiv0 as apiv0_ep
from voeventdb.remote.keys import FilterKeys
from voeventdb.server.tests.fixtures.connection import simple_populated_db
import voeventdb.server.tests.fixtures.fake as fake
import datetime

@pytest.mark.usefixtures('mock_requests','simple_populated_db')
class TestGetSummaryWraps():
    def test_default_params(self,simple_populated_db):
        dbinf = simple_populated_db
        count = wrappers.get_summary_data(endpoint=apiv0_ep.count,
                                          filters=None,
                                          host=vr.default_host)
        assert count == dbinf.n_inserts

    def test_filter_by_datetime(self,simple_populated_db):
        """
        Turns out that requests autoformats datetimes, jolly good.
        """
        dbinf = simple_populated_db
        filters = {
            FilterKeys.authored_since : fake.default_start_dt + datetime.timedelta(days=1)
        }
        count = wrappers.get_summary_data(endpoint=apiv0_ep.count,
                                          filters=filters,
                                          host=vr.default_host)
        assert count != dbinf.n_inserts
        assert count < dbinf.n_inserts
        assert count != 0


