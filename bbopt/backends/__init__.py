#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x25751311

# Compiled with Coconut version 1.3.0-post_dev3 [Dead Parrot]

"""
Backends contains all of bbopt's different backends.
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



class BackendRegistry(_coconut.object):
    def _coconut_lambda_1(_=None):
        from bbopt.backends.serving import ServingBackend
        return ServingBackend
    def _coconut_lambda_2(_=None):
        from bbopt.backends.random import RandomBackend
        return RandomBackend
    def _coconut_lambda_3(_=None):
        from bbopt.backends.skopt import SkoptBackend
        return SkoptBackend
    def _coconut_lambda_4(_=None):
        from bbopt.backends.hypteropt import HyperoptBackend
        return HyperoptBackend
    backend_generators = {"serving": (_coconut_lambda_1), "random": (_coconut_lambda_2), "scikit-optimize": (_coconut_lambda_3), "hyperopt": (_coconut_lambda_4)}
    registered_backends = {}

    def __getitem__(self, name):
        if name is None:
            name = "serving"
        if name in self.registered_backends:
            return self.registered_backends[name]
        elif name in self.backend_generators:
            backend = self.backend_generators[name]()
            del self.backend_generators[name]
            self.registered_backends[name] = backend
            return backend
        else:
            raise ValueError("unknown backend %r" % name)

    def __iter__(self):
        _coconut_yield_from = backend_generators
        for _coconut_yield_item in _coconut_yield_from:
            yield _coconut_yield_item

        _coconut_yield_from = registered_backends
        for _coconut_yield_item in _coconut_yield_from:
            yield _coconut_yield_item


    def register_backend(self, name, backend):
        """Register a new backend under the given name."""
        self.registered_backends[name] = backend

    def init_backend(self, name, examples, params, **kwargs):
        """Create a backend object of the given name with the given example data."""
        return self[name](examples, params, **kwargs)

backend_registry = BackendRegistry()
