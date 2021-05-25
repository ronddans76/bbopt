#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x65e04e94

# Compiled with Coconut version 1.5.0-post_dev49 [Fish License]

"""
Utilities for use in BBopt backends.
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



if _coconut_sys.version_info < (3, 3):
    from collections import Iterable
else:
    from collections.abc import Iterable

from bbopt.util import sorted_items
from bbopt.params import param_processor
from bbopt.registry import backend_registry
from bbopt.registry import alg_registry


# Utilities:

def negate_objective(objective):
    """Take the negative of the given objective (converts a gain into a loss and vice versa)."""
    if isinstance(objective, Iterable):
        return (list)((map)(negate_objective, objective))
    else:
        return -objective


def make_features(values, params, fallback_func=param_processor.choose_default_placeholder, converters={}, convert_fallback=True,):
    """Return an iterator of the values for the parameters in sorted order with the given fallback function.
    If passed, converters must map funcs to functions from (value, *args) -> new_value which will be run
    on the resulting value for that func (but only on fallbacks if convert_fallback)."""
    for name, (func, args, kwargs) in sorted_items(params):
# determine feature
        fallback = False
        _coconut_match_to_1 = values
        _coconut_match_check_1 = False
        if _coconut.isinstance(_coconut_match_to_1, _coconut.abc.Mapping):
            _coconut_match_temp_0 = _coconut_match_to_1.get(name, _coconut_sentinel)
            if _coconut_match_temp_0 is not _coconut_sentinel:
                feature = _coconut_match_temp_0
                _coconut_match_check_1 = True
        if _coconut_match_check_1:
            pass
        else:
            _coconut_match_to_0 = kwargs
            _coconut_match_check_0 = False
            if _coconut.isinstance(_coconut_match_to_0, _coconut.abc.Mapping):
                _coconut_match_temp_0 = _coconut_match_to_0.get("placeholder_when_missing", _coconut_sentinel)
                if _coconut_match_temp_0 is not _coconut_sentinel:
                    placeholder_value = _coconut_match_temp_0
                    _coconut_match_check_0 = True
            if _coconut_match_check_0:
                feature = placeholder_value
            else:
                fallback = True
                feature = fallback_func(name, func, *args, **kwargs)

# run converters
        if not fallback or convert_fallback:
            _coconut_match_to_2 = converters
            _coconut_match_check_2 = False
            if _coconut.isinstance(_coconut_match_to_2, _coconut.abc.Mapping):
                _coconut_match_temp_0 = _coconut_match_to_2.get(func, _coconut_sentinel)
                if _coconut_match_temp_0 is not _coconut_sentinel:
                    converter_func = _coconut_match_temp_0
                    _coconut_match_check_2 = True
            if _coconut_match_check_2:
                feature = converter_func(feature, *args)

        yield feature


def get_names_and_features(values, params, *args, **kwargs):
    """Same as make_features but yields (name, feature) instead of just feature."""
    _coconut_yield_from_1 = _coconut.iter(zip(sorted(params), make_features(values, params, *args, **kwargs)))
    while True:
        try:
            yield _coconut.next(_coconut_yield_from_1)
        except _coconut.StopIteration as _coconut_yield_err_0:
            _coconut_yield_from_0 = _coconut_yield_err_0.args[0] if _coconut.len(_coconut_yield_err_0.args) > 0 else None
            break

    _coconut_yield_from_0


def split_examples(examples, params, fallback_func=param_processor.choose_default_placeholder, converters={}, convert_fallback=True,):
    """Split examples into a list of data points and a list of losses with the given fallback function."""
    data_points, losses = [], []
    for example in examples:

# extract values, loss
        _coconut_case_match_to_0 = example
        _coconut_case_match_check_0 = False
        if _coconut.isinstance(_coconut_case_match_to_0, _coconut.abc.Mapping):
            _coconut_match_temp_0 = _coconut_case_match_to_0.get("values", _coconut_sentinel)
            _coconut_match_temp_1 = _coconut_case_match_to_0.get("gain", _coconut_sentinel)
            if (_coconut_match_temp_0 is not _coconut_sentinel) and (_coconut_match_temp_1 is not _coconut_sentinel):
                values = _coconut_match_temp_0
                gain = _coconut_match_temp_1
                _coconut_case_match_check_0 = True
        if _coconut_case_match_check_0:
            loss = negate_objective(gain)
        if not _coconut_case_match_check_0:
            if _coconut.isinstance(_coconut_case_match_to_0, _coconut.abc.Mapping):
                _coconut_match_temp_0 = _coconut_case_match_to_0.get("values", _coconut_sentinel)
                _coconut_match_temp_1 = _coconut_case_match_to_0.get("loss", _coconut_sentinel)
                if (_coconut_match_temp_0 is not _coconut_sentinel) and (_coconut_match_temp_1 is not _coconut_sentinel):
                    values = _coconut_match_temp_0
                    loss = _coconut_match_temp_1
                    _coconut_case_match_check_0 = True
            if _coconut_case_match_check_0:
                pass
        if not _coconut_case_match_check_0:
            raise ValueError("invalid example {_coconut_format_0}".format(_coconut_format_0=(example)))

# extract features
        features = (list)(make_features(values, params, fallback_func, converters, convert_fallback))

# add to data_points, losses
        (data_points.append)(features)
        (losses.append)(loss)

    return data_points, losses


def get_named_data_points_and_losses(examples, params, *args, **kwargs):
    """Same as split_examples but returns named_data_points instead of data_points."""
    sorted_names = list(sorted(params))
    data_points, losses = split_examples(examples, params, *args, **kwargs)
    named_data_points = []
    for point in data_points:
        pt_val = {}
        for name, item in zip(sorted_names, point):
            pt_val[name] = item
        named_data_points.append(pt_val)
    return named_data_points, losses


def make_values(params, point):
    """Return a dictionary with the values replaced by the values in point,
    where point is a list of the values corresponding to the sorted params."""
    values = {}
    for i, k in (enumerate)((sorted)(params)):
        values[k] = point[i]
    return values


def serve_values(name, func, args, kwargs, serving_values, fallback_func, backend_name=None, implemented_funcs=None, supported_kwargs=None,):
    """Determines the parameter value to serve for the given parameter
    name and kwargs. First checks for unsupported funcs or kwargs, then
    uses the following algorithm:
    1. if name in serving_values, use serving_values[name], else
    2. if guess in kwargs, use the guess, else
    3. call fallback_func(name, func, *args, **kwargs)."""
# validate arguments
    if implemented_funcs is not None:
        assert backend_name is not None, "serve_values expects a backend_name argument when doing func validation"
        if func not in implemented_funcs:
            raise ValueError("the {_coconut_format_0} backend does not implement the {_coconut_format_1} function".format(_coconut_format_0=(backend_name), _coconut_format_1=(func)))
    if supported_kwargs is not None:
        assert backend_name is not None, "serve_values expects a backend_name argument when doing kwargs validation"
        unsupported_kwargs = set(kwargs) - set(supported_kwargs)
        if unsupported_kwargs:
            raise ValueError("the {_coconut_format_0} backend does not support {_coconut_format_1} option(s)".format(_coconut_format_0=(backend_name), _coconut_format_1=(unsupported_kwargs)))

# determine value
    _coconut_match_to_4 = serving_values
    _coconut_match_check_4 = False
    if _coconut.isinstance(_coconut_match_to_4, _coconut.abc.Mapping):
        _coconut_match_temp_0 = _coconut_match_to_4.get(name, _coconut_sentinel)
        if _coconut_match_temp_0 is not _coconut_sentinel:
            value = _coconut_match_temp_0
            _coconut_match_check_4 = True
    if _coconut_match_check_4:
        return value
    else:
        _coconut_match_to_3 = kwargs
        _coconut_match_check_3 = False
        if _coconut.isinstance(_coconut_match_to_3, _coconut.abc.Mapping):
            _coconut_match_temp_0 = _coconut_match_to_3.get("guess", _coconut_sentinel)
            if _coconut_match_temp_0 is not _coconut_sentinel:
                guess = _coconut_match_temp_0
                _coconut_match_check_3 = True
        if _coconut_match_check_3:
            return guess
        else:
            return fallback_func(name, func, *args, **kwargs)


# Backend base classes:

class Backend(_coconut.object):
    """Base class for all BBopt backends."""
# derived classes should always set this
    backend_name = None

# derived classes can modify these if they want to further
#  restrict the set of supported funcs and/or kwargs
    implemented_funcs = None
    supported_kwargs = ("guess", "placeholder_when_missing",)

# derived classes must set this on each run if they want to
#  use the default param implementation
    current_values = None

# derived classes must set this if they want to use the
#  default fallback_func implementation
    fallback_backend = None

# derived classes can implement tell_examples(new_examples)
#  to allow fast updating on new data
    tell_examples = None

    def __new__(cls, examples=None, params=None, *args, **kwargs):
        self = super(Backend, cls).__new__(cls)
        if self.tell_examples is not None:
            self._examples = examples
            self._params = params
            self._args = args
            self._kwargs = kwargs
        return self

    def __init__(self, examples=None, params=None):
        pass

    def attempt_update(self, examples=None, params=None, *args, **kwargs):
        """Attempt to update this backend with new arguments. False indicates that the
        update failed while True indicates a successful update."""
        if (self.tell_examples is None or not self._params or params != self._params or args != self._args or kwargs != self._kwargs):
            return False
        old_examples, new_examples = examples[:len(self._examples)], examples[len(self._examples):]
        if old_examples != self._examples:
            return False
        if new_examples:
            try:
                self.tell_examples(new_examples)
            except NotImplementedError:
                return False
        return True

    def init_fallback_backend(self):
        """Set fallback_backend to a new random backend instance."""
        self.fallback_backend = backend_registry["random"]()

    def fallback_func(self, name, func, *args, **kwargs):
        """Default fallback_func calls self.fallback_backend.param."""
        assert self.fallback_backend is not None, "Backend subclasses using Backend.fallback_func must set fallback_backend"
        return self.fallback_backend.param(name, func, *args, **kwargs)

    def param(self, name, func, *args, **kwargs):
        """Default param calls serve_values with self.current_values and self.fallback_func."""
        assert self.current_values is not None, "Backend subclasses using Backend.param must set current_values"
        return serve_values(name, func, args, kwargs, serving_values=self.current_values, fallback_func=self.fallback_func, backend_name=self.backend_name, implemented_funcs=self.implemented_funcs, supported_kwargs=self.supported_kwargs)

    @classmethod
    def register(cls):
        """Register this backend to the backend registry."""
        assert cls.backend_name is not None, "Backend subclasses using Backend.register must set backend_name on the class"
        backend_registry.register(cls.backend_name, cls)

    @classmethod
    def register_alg(cls, alg_name, **options):
        """Register an algorithm under the given name that calls this backend with the given options."""
        assert cls.backend_name is not None, "Backend subclasses using Backend.register_alg must set backend_name on the class"
        alg_registry.register(alg_name, (cls.backend_name, options))

    @classmethod
    def register_alias(cls, alias):
        """Register an alias for this backend."""
        assert cls.backend_name is not None, "Backend subclasses using Backend.register_alias must set backend_name on the class"
        backend_registry.register_alias(cls.backend_name, alias)

    @staticmethod
    def register_param_func(func_name, handler, placeholder_generator, support_check_func):
        """Register a new parameter definition function. See bbopt.params for examples."""
        param_processor.register(func_name, handler, placeholder_generator, support_check_func)


_coconut_call_set_names(Backend)
class StandardBackend(Backend):
    """Base class for standard BBopt backends."""

    def __init__(self, examples, params, *args, **kwargs):
        self.init_fallback_backend()

        if not params:
            self.current_values = {}
            return

        self.setup_backend(params, *args, **kwargs)

        if examples:
            self.tell_examples(examples)
        else:
            self.current_values = {}

    @override
    def tell_examples(self, new_examples):
        """Implements tell_examples by calling tell_data."""
        new_data, new_losses = get_named_data_points_and_losses(new_examples, self._params)
        self.tell_data(new_data, new_losses)
        self.current_values = self.get_next_values()

    def setup_backend(self, params, *args, **kwargs):
        """Override setup_backend with any setup work that needs to be done."""
        raise NotImplementedError("StandardBackend subclasses using StandardBackend.__init__ must define a setup_backend(params, *args, **kwargs) method")

    def tell_data(self, new_data, new_losses):
        """Override tell_data with any work that needs to be done to add the given data and losses."""
        raise NotImplementedError("StandardBackend subclasses using StandardBackend.tell_examples must define a tell_data(new_data, new_losses) method")

    def get_next_values(self):
        """Override get_next_values to produce the next set of values that should be evaluated."""
        raise NotImplementedError("StandardBackend subclasses using StandardBackend.tell_examples must define a get_next_values() method")

_coconut_call_set_names(StandardBackend)
