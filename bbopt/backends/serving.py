#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x3812c675

# Compiled with Coconut version 1.5.0-post_dev49 [Fish License]

"""
The serving backend. Selects the best existing data point.
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



from bbopt.util import best_example
from bbopt.backends.util import Backend


class ServingBackend(Backend):
    """The serving backend uses the parameter values from the best example."""
    backend_name = "serving"

    def __init__(self, examples, params):
        self.attempt_update(examples, params)

    @override
    def fallback_func(self, name, func, *args, **kwargs):
        raise ValueError("missing data for parameter {_coconut_format_0} while serving and no guess".format(_coconut_format_0=(name)))

    @override
    def attempt_update(self, examples, params):
        """Update the serving backend with new parameters."""
# since we're serving, ignore params and just extract the best example
        self.current_values = best_example(examples)["values"]
        return True


# Registered names:

_coconut_call_set_names(ServingBackend)
ServingBackend.register()
ServingBackend.register_alias(None)
ServingBackend.register_alg("serving")
ServingBackend.register_alg(None)
