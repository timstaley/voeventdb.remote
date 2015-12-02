from __future__ import print_function
import pytest
import inspect
import voeventdb.remote.apiv0 as apiv0
from voeventdb.remote.keys import FilterKeys

import logging
logger = logging.getLogger(__name__)

apiv0_funcs_dict = {k:v for k,v in vars(apiv0).items()
               if inspect.isfunction(v)}

apiv0_queryfuncs_dict = apiv0_funcs_dict.copy()
apiv0_queryfuncs_dict.pop('synopsis')
apiv0_queryfuncs_dict.pop('xml')

@pytest.mark.usefixtures('mock_requests')
@pytest.mark.parametrize("funcname,func",
                             tuple(apiv0_queryfuncs_dict.items())
                             )
class TestFunctionCalls():
    def test_queryfuncs_with_default_params(self, simple_populated_db,
                                          funcname, func):
        logger.debug("Testing{}".format(funcname))
        results = func()
        # print(results)

    def test_queryfuncs_with_filter(self, simple_populated_db,
                                   funcname, func):
        logger.debug("Testing{}".format(funcname))
        filter = {FilterKeys.ivorn_prefix:'ivo://',
                  FilterKeys.role:'utility'}
        results = func(filters=filter)
        # print(results)

