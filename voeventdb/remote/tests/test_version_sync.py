from __future__ import print_function
import pytest
import voeventdb.server.restapi.inspection_utils as iu
import voeventdb.remote.apiv1 as apiv1
from voeventdb.remote.apiv1 import FilterKeys


def test_filterkeys_sync():
    server_filterkeys = iu.queryfilter_keys_and_examples_values().keys()
    remote_filterkeys = [getattr(FilterKeys, v)
                         for v in vars(FilterKeys) if not v.startswith('__')]
    assert set(server_filterkeys) == set(remote_filterkeys)


