#!/usr/bin/env python
"""A small wrapper around nosetests.
Turns down the iso8601 logging level-
otherwise this can be disruptive when viewing error messages.
"""
import sys

import pytest

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)  
    logging.getLogger('iso8601').setLevel(logging.ERROR) #Suppress iso8601 debug log.
    sys.exit(pytest.main())
