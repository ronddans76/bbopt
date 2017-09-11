#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xb563af77

# Compiled with Coconut version 1.3.0-post_dev2 [Dead Parrot]

"""
The random backend. Used for testing purposes.
Does not use existing data, simply spits out random valid values.
"""

# Coconut Header: -------------------------------------------------------------

from __future__ import print_function, absolute_import, unicode_literals, division
import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.abspath(__file__))
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import _coconut, _coconut_NamedTuple, _coconut_MatchError, _coconut_igetitem, _coconut_base_compose, _coconut_forward_compose, _coconut_back_compose, _coconut_forward_star_compose, _coconut_back_star_compose, _coconut_pipe, _coconut_star_pipe, _coconut_back_pipe, _coconut_back_star_pipe, _coconut_bool_and, _coconut_bool_or, _coconut_none_coalesce, _coconut_minus, _coconut_map, _coconut_partial
from __coconut__ import *
_coconut_sys.path.remove(_coconut_file_path)

# Compiled Coconut: -----------------------------------------------------------



# Imports:

import random

# Backend:

class RandomBackend(_coconut.object):
    """RandomBackend chooses random valid values."""

    def __init__(self, examples):
        pass  # we're choosing randomly, so we ignore the given example data!

    def param(self, name, choose_from):
        return random.choice(choose_from)
