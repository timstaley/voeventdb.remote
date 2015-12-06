from __future__ import print_function
import pytest
from voeventdb.server.tests.resources import swift_bat_grb_655721
import voeventdb.remote.apiv0 as apiv0
import voeventparse as vp
import requests
import logging
logger = logging.getLogger(__name__)

from voeventdb.remote.helpers import Synopsis

@pytest.mark.usefixtures('mock_requests')
class TestFunctionCalls():
    def test_ordering_param(self, simple_populated_db):
        """Just a sanity check that ordering syntax is correct"""
        dbinf = simple_populated_db
        all_ivorns = apiv0.ivorn(order=apiv0.OrderValues.id)
        all_ivorns_rev_order = apiv0.ivorn(order=apiv0.OrderValues.id_desc)
        assert all_ivorns == dbinf.inserted_ivorns
        assert all_ivorns_rev_order == all_ivorns[::-1]

    def test_xml_retrieval(self, simple_populated_db):
        dbinf = simple_populated_db
        all_ivorns = apiv0.ivorn(order=apiv0.OrderValues.id)
        xml = apiv0.xml(all_ivorns[-1])
        assert xml == vp.dumps(dbinf.insert_packets[-1])

        #Now try a non-existent ivorn:
        with pytest.raises(requests.HTTPError):
            apiv0.xml('ivo://foo/bar')

    def test_synopsis(self, simple_populated_db):
        """Check synopsis wrapper function, helper class."""
        dbinf = simple_populated_db

        # Try an packet with references
        ivorns_w_refs = apiv0.ivorn(
            filters={apiv0.FilterKeys.ref: True},
            order = apiv0.OrderValues.id,
        )
        s = Synopsis(apiv0.synopsis(ivorns_w_refs[0]))
        assert s.references
        assert len(s.sky_events) == 0

        #Now try a non-existent ivorn:
        with pytest.raises(requests.HTTPError):
            apiv0.synopsis('ivo://foo/bar')

        # Now try a packet with co-ords
        sb_ivorn = swift_bat_grb_655721.attrib['ivorn']
        assert sb_ivorn in dbinf.inserted_ivorns
        s = Synopsis(apiv0.synopsis(sb_ivorn))
        assert s.coords
        assert len(s.coords) == 1
        skyevent = s.sky_events[0]
        c_pkt = vp.pull_astro_coords(swift_bat_grb_655721)
        assert skyevent.position.ra.value == c_pkt.ra
        assert skyevent.position.dec.value == c_pkt.dec
        assert skyevent.position_error.value == c_pkt.err


