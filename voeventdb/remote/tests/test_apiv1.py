from __future__ import print_function

import logging

import pytest
import requests

import voeventdb.remote as vr
import voeventdb.remote.apiv1 as apiv1
import voeventdb.remote.apiv1.definitions
import voeventdb.server.restapi.inspection_utils as iu
import voeventparse as vp
from voeventdb.remote.helpers import Synopsis
from voeventdb.server.restapi.v1.definitions import _list_class_vars
from voeventdb.server.tests.resources import swift_bat_grb_655721

logger = logging.getLogger(__name__)


def test_endpoint_urls_in_sync():
    v1_ep_upstream = iu.apiv1_endpoints().values()
    v1_ep_remote = _list_class_vars(vr.apiv1.definitions.Endpoints).values()
    assert  sorted(v1_ep_upstream) == sorted(v1_ep_remote)


@pytest.mark.usefixtures('mock_requests')
class TestFunctionCalls():
    def test_ordering_param(self, simple_populated_db):
        """Just a sanity check that ordering syntax is correct"""
        dbinf = simple_populated_db
        all_ivorns = apiv1.list_ivorn(order=apiv1.OrderValues.id)
        all_ivorns_rev_order = apiv1.list_ivorn(order=apiv1.OrderValues.id_desc)
        assert all_ivorns == dbinf.inserted_ivorns
        assert all_ivorns_rev_order == all_ivorns[::-1]

    def test_list_pagination(self, simple_populated_db,
                            reset_globals_to_defaults):
        """
        Sanity check that pagination params passed correctly to wrapper func.

        (NB wrapper tested independently elsewhere).
        """
        vr.default_list_n_max = 30
        vr.default_pagesize = 5
        dbinf = simple_populated_db
        count = apiv1.count()
        assert count > vr.default_list_n_max
        ivorns = apiv1.list_ivorn()
        assert len(ivorns) == vr.default_list_n_max
        #This time we override the max:
        ivorns = apiv1.list_ivorn(n_max=0)
        assert len(ivorns) == dbinf.n_inserts

    def test_xml_retrieval(self, simple_populated_db):
        dbinf = simple_populated_db
        all_ivorns = apiv1.list_ivorn(order=apiv1.OrderValues.id)
        xml = apiv1.packet_xml(all_ivorns[-1])
        assert xml == vp.dumps(dbinf.insert_packets[-1])

        #Now try a non-existent ivorn:
        with pytest.raises(requests.HTTPError):
            apiv1.packet_xml('ivo://foo/bar')

    def test_synopsis(self, simple_populated_db):
        """Check synopsis wrapper function, helper class."""
        dbinf = simple_populated_db

        # Try an packet with references
        ivorns_w_refs = apiv1.list_ivorn(
            filters={apiv1.FilterKeys.ref_any: True},
            order = apiv1.OrderValues.id,
        )
        s = Synopsis(apiv1.packet_synopsis(ivorns_w_refs[0]))
        assert s.references
        assert len(s.sky_events) == 0

        #Now try a non-existent ivorn:
        with pytest.raises(requests.HTTPError):
            apiv1.packet_synopsis('ivo://foo/bar')

        # Now try a packet with co-ords
        sb_ivorn = swift_bat_grb_655721.attrib['ivorn']
        assert sb_ivorn in dbinf.inserted_ivorns
        s = Synopsis(apiv1.packet_synopsis(sb_ivorn))
        assert s.coords
        assert len(s.coords) == 1
        skyevent = s.sky_events[0]
        c_pkt = vp.get_event_position(swift_bat_grb_655721)
        assert skyevent.position.ra.value == c_pkt.ra
        assert skyevent.position.dec.value == c_pkt.dec
        assert skyevent.position_error.value == c_pkt.err
