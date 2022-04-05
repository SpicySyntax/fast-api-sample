""" Run all pytests """

import pytest
from autohooks.api.git import get_staged_status
from autohooks.api.path import match
from autohooks.api import ok # pylint:disable=undefined-variable

DEFAULT_INCLUDE = ('*.py',)

def precommit(**kwargs): # pylint:disable=unused-argument
    files = [f for f in get_staged_status() if match(f.path, DEFAULT_INCLUDE)]
    if len(files) == 0:
        ok('No staged files for black available.') # pylint:disable=undefined-variable
        return 0
    return pytest.console_main()
