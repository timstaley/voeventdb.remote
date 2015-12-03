from __future__ import print_function
import pytest
import voeventdb.remote as vr
import voeventdb.remote.request_wrappers as wrappers

from voeventdb.remote.apiv0 import Endpoints, FilterKeys

from voeventdb.server.tests.fixtures.connection import simple_populated_db
import voeventdb.server.tests.fixtures.fake as fake
import datetime
import iso8601


@pytest.mark.usefixtures('mock_requests', 'simple_populated_db')
class TestGetSummaryWraps():
    def test_default_params(self, simple_populated_db):
        dbinf = simple_populated_db
        count = wrappers.get_summary_data(endpoint=Endpoints.count,
                                          filters=None,
                                          host=vr.default_host)
        assert count == dbinf.n_inserts

    def test_filter_by_datetime(self, simple_populated_db):
        """
        Turns out that requests autoformats datetimes, jolly good.
        """
        dbinf = simple_populated_db
        cutoff_time = fake.default_start_dt + datetime.timedelta(days=0.75)
        filters = {
            FilterKeys.authored_since: cutoff_time
        }

        qualifying_packets = [p for p in dbinf.insert_packets
                              if iso8601.parse_date(p.Who.Date.text) >= cutoff_time]

        count = wrappers.get_summary_data(endpoint=Endpoints.count,
                                          filters=filters,
                                          host=vr.default_host)
        assert count != 0
        assert count < dbinf.n_inserts
        assert count == len(qualifying_packets)
