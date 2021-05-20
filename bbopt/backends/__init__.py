#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xac837e9d

# Compiled with Coconut version 1.5.0-post_dev45 [Fish License]

"""
Backends contains all of bbopt's different backends.
"""

# Coconut Header: -------------------------------------------------------------

from __future__ import print_function, absolute_import, unicode_literals, division
import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.dirname(_coconut_os_path.abspath(__file__)))
_coconut_cached_module = _coconut_sys.modules.get(str("__coconut__"))
if _coconut_cached_module is not None and _coconut_os_path.dirname(_coconut_cached_module.__file__) != _coconut_file_path:
    del _coconut_sys.modules[str("__coconut__")]
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import *
from __coconut__ import _coconut_call_set_names, _coconut, _coconut_MatchError, _coconut_igetitem, _coconut_base_compose, _coconut_forward_compose, _coconut_back_compose, _coconut_forward_star_compose, _coconut_back_star_compose, _coconut_forward_dubstar_compose, _coconut_back_dubstar_compose, _coconut_pipe, _coconut_star_pipe, _coconut_dubstar_pipe, _coconut_back_pipe, _coconut_back_star_pipe, _coconut_back_dubstar_pipe, _coconut_none_pipe, _coconut_none_star_pipe, _coconut_none_dubstar_pipe, _coconut_bool_and, _coconut_bool_or, _coconut_none_coalesce, _coconut_minus, _coconut_map, _coconut_partial, _coconut_get_function_match_error, _coconut_base_pattern_func, _coconut_addpattern, _coconut_sentinel, _coconut_assert, _coconut_mark_as_match, _coconut_reiterable
if _coconut_sys.version_info >= (3,):
    _coconut_sys.path.pop(0)

# Compiled Coconut: -----------------------------------------------------------



sys = _coconut_sys
import traceback

# import all the other backends to register them
from bbopt.backends.serving import ServingBackend
from bbopt.backends.random import RandomBackend
from bbopt.backends.mixture import MixtureBackend
try:
    from bbopt.backends.skopt import SkoptBackend
except ImportError:
    traceback.print_exc()
    print("Could not import scikit-optimize backend; backend unavailable (see above error).")
try:
    from bbopt.backends.hyperopt import HyperoptBackend
except ImportError:
    traceback.print_exc()
    print("Could not import hyperopt backend; backend unavailable (see above error).")
if sys.version_info >= (3,):
    try:
        from bbopt.backends.pysot import PySOTBackend
    except ImportError:
        traceback.print_exc()
        print("Could not import pySOT backend; backend unavailable (see above error).")
if sys.version_info >= (3, 7):
    try:
        from bbopt.backends.bask import BaskBackend
    except ImportError:
        traceback.print_exc()
        print("Could not import bayes-skopt backend; backend unavailable (see above error).")
