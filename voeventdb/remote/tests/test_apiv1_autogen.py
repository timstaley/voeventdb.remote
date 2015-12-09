from __future__ import print_function
import pytest
import inspect
import voeventdb.remote.apiv1 as apiv1
from voeventdb.remote.apiv1 import FilterKeys

import logging

logger = logging.getLogger(__name__)

apiv1_funcs_dict = {k: v for k, v in vars(apiv1).items()
                    if inspect.isfunction(v)
                    and not k.startswith('_')}

apiv1_queryfuncs_dict = apiv1_funcs_dict.copy()
apiv1_queryfuncs_dict.pop('synopsis')
apiv1_queryfuncs_dict.pop('xml')
apiv1_queryfuncs_dict.pop('citation_network_map')


@pytest.mark.usefixtures('mock_requests')
@pytest.mark.parametrize("funcname,func",
                         tuple(apiv1_queryfuncs_dict.items())
                         )
class TestFunctionCalls():
    def test_queryfuncs(self, simple_populated_db,
                        funcname, func):
        logger.debug("Testing{}".format(funcname))

        # Test with default params:
        results = func()
        # print(results)

        # Test with a filter applied:
        filter = {FilterKeys.ivorn_prefix: 'ivo://',
                  FilterKeys.role: 'utility'}
        results = func(filters=filter)
