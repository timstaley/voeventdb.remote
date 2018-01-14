from __future__ import print_function

import datetime

import astropy.units as units
import iso8601
import pytest
import requests
from astropy.coordinates import Angle, SkyCoord

import voeventdb.remote as vr
import voeventdb.remote.request_wrappers as wrappers
import voeventdb.server.tests.fixtures.fake as fake
from voeventdb.remote.apiv1.definitions import Endpoints, FilterKeys
from voeventdb.remote.definitions import ResultKeys
from voeventdb.server.tests.fixtures.connection import simple_populated_db


@pytest.mark.usefixtures('mock_requests', 'simple_populated_db')
class TestGetSummaryWraps():
    def test_default_params(self, simple_populated_db):
        dbinf = simple_populated_db
        count = wrappers.get_summary_data(endpoint=Endpoints.count,
                                          filters=None,
                                          host=vr.default_host)
        assert count == dbinf.n_inserts

    def test_list_wrapper_pagination(self, simple_populated_db,
                                     reset_globals_to_defaults):
        vr.default_list_n_max = 30
        vr.default_pagesize = 5
        dbinf = simple_populated_db
        count = wrappers.get_summary_data(endpoint=Endpoints.count,
                                          filters=None,
                                          host=vr.default_host)
        assert count > vr.default_list_n_max
        ivorns = wrappers.get_list_data(
            list_endpoint=Endpoints.list_ivorn,
            count_endpoint=Endpoints.count,
        )
        assert len(ivorns) == vr.default_list_n_max

        # This time we override the max:
        ivorns = wrappers.get_list_data(
            list_endpoint=Endpoints.list_ivorn,
            count_endpoint=Endpoints.count,
            n_max=0,
        )
        assert len(ivorns) == dbinf.n_inserts

    def test_filter_by_datetime(self, simple_populated_db):
        """
        Check default requests behaviour when passed datetime-params.
        """
        dbinf = simple_populated_db
        cutoff_time = fake.default_start_dt + datetime.timedelta(days=0.75)
        filters = {
            FilterKeys.authored_since: cutoff_time
        }

        qualifying_packets = [p for p in dbinf.insert_packets
                              if iso8601.parse_date(
                p.Who.Date.text) >= cutoff_time]

        # Grab a copy of the full response dict to check that datetimes
        # are acceptably formatted by requests:
        rv = wrappers.get_summary_response(endpoint=Endpoints.count,
                                           filters=filters,
                                           host=vr.default_host)
        rd = rv.json()
        dt_string = rd[ResultKeys.querystring][FilterKeys.authored_since][0]
        assert iso8601.parse_date(dt_string) == cutoff_time

        count = wrappers.get_summary_data(endpoint=Endpoints.count,
                                          filters=filters,
                                          host=vr.default_host)
        assert count != 0
        assert count < dbinf.n_inserts
        assert count == len(qualifying_packets)


class TestConeParamParsing():
    @pytest.fixture(autouse=True)
    def assign_test_values(self):
        self.posn = SkyCoord(180, 0, unit='deg')
        self.posn_err = Angle(5, unit='deg')
        self.cone = (self.posn, self.posn_err)
        self.cone_string = str(
            [self.posn.ra.deg, self.posn.dec.deg, self.posn_err.deg])

    def test_string_format_still_valid(self, mock_requests):
        rv = requests.get(url=vr.default_host + Endpoints.count,
                          params={FilterKeys.cone: self.cone_string})
        # print(rv.text)
        assert rv.status_code == 200

    def test_bad_arg(self):
        with pytest.raises(TypeError):
            wrappers.format_conesearch_params()
        with pytest.raises(ValueError):
            wrappers.format_conesearch_params(None)
        with pytest.raises(ValueError):
            wrappers.format_conesearch_params("foobar")
        with pytest.raises(TypeError):
            wrappers.format_conesearch_params(42)
        with pytest.raises(TypeError):
            wrappers.format_conesearch_params((1,2,3,4))

    def test_valid_string_passthrough(self):
        assert (wrappers.format_conesearch_params(self.cone_string) ==
                self.cone_string)

    def test_skycoord_angle_pair(self):
        input = (self.posn, self.posn_err)
        assert wrappers.format_conesearch_params(input) == self.cone_string

    def test_skycoord_units_pair(self):
        input = (self.posn, self.posn_err.deg * units.deg)
        assert wrappers.format_conesearch_params(input) == self.cone_string

    def test_float_tuple(self):
        input = (self.posn.ra.deg, self.posn.dec.deg, self.posn_err.deg)
        assert wrappers.format_conesearch_params(input) == self.cone_string
