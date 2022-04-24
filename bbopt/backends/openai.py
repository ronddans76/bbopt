#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x1e287463

# Compiled with Coconut version 2.0.0-a_dev53 [How Not to Be Seen]

"""
The OpenAI backend. Uses large language models for black box optimization.
"""

# Coconut Header: -------------------------------------------------------------

from __future__ import print_function, absolute_import, unicode_literals, division
import sys as _coconut_sys, os as _coconut_os
_coconut_file_dir = _coconut_os.path.dirname(_coconut_os.path.dirname(_coconut_os.path.abspath(__file__)))
_coconut_cached_module = _coconut_sys.modules.get(str("__coconut__"))
if _coconut_cached_module is not None and _coconut_os.path.dirname(_coconut_cached_module.__file__) != _coconut_file_dir:  # type: ignore
    del _coconut_sys.modules[str("__coconut__")]
_coconut_sys.path.insert(0, _coconut_file_dir)
_coconut_module_name = _coconut_os.path.splitext(_coconut_os.path.basename(_coconut_file_dir))[0]
if _coconut_module_name and _coconut_module_name[0].isalpha() and all(c.isalpha() or c.isdigit() for c in _coconut_module_name) and "__init__.py" in _coconut_os.listdir(_coconut_file_dir):
    _coconut_full_module_name = str(_coconut_module_name + ".__coconut__")
    import __coconut__ as _coconut__coconut__
    _coconut__coconut__.__name__ = _coconut_full_module_name
    for _coconut_v in vars(_coconut__coconut__).values():
        if getattr(_coconut_v, "__module__", None) == str("__coconut__"):
            try:
                _coconut_v.__module__ = _coconut_full_module_name
            except AttributeError:
                _coconut_v_type = type(_coconut_v)
                if getattr(_coconut_v_type, "__module__", None) == str("__coconut__"):
                    _coconut_v_type.__module__ = _coconut_full_module_name
    _coconut_sys.modules[_coconut_full_module_name] = _coconut__coconut__
from __coconut__ import *
from __coconut__ import _coconut_call_set_names, _coconut_handle_cls_kwargs, _coconut_handle_cls_stargs, _namedtuple_of, _coconut, _coconut_super, _coconut_MatchError, _coconut_iter_getitem, _coconut_base_compose, _coconut_forward_compose, _coconut_back_compose, _coconut_forward_star_compose, _coconut_back_star_compose, _coconut_forward_dubstar_compose, _coconut_back_dubstar_compose, _coconut_pipe, _coconut_star_pipe, _coconut_dubstar_pipe, _coconut_back_pipe, _coconut_back_star_pipe, _coconut_back_dubstar_pipe, _coconut_none_pipe, _coconut_none_star_pipe, _coconut_none_dubstar_pipe, _coconut_bool_and, _coconut_bool_or, _coconut_none_coalesce, _coconut_minus, _coconut_map, _coconut_partial, _coconut_get_function_match_error, _coconut_base_pattern_func, _coconut_addpattern, _coconut_sentinel, _coconut_assert, _coconut_raise, _coconut_mark_as_match, _coconut_reiterable, _coconut_self_match_types, _coconut_dict_merge, _coconut_exec, _coconut_comma_op, _coconut_multi_dim_arr, _coconut_mk_anon_namedtuple
_coconut_sys.path.pop(0)

# Compiled Coconut: -----------------------------------------------------------



import os
from ast import literal_eval

import openai

from bbopt.params import param_processor
from bbopt.backends.util import StandardBackend


# Utilities:

def get_prompt(params, data_points, losses):
    return '''# black box function to be minimized
def f({func_params}) -> float:
    """
    parameters:
{docstring}

    returns:
        float: the loss
    """
    return black_box_function({names})

# known values (should converge to minimum of f)
{values}
assert f('''.format(func_params=", ".join(("{name}: {type}".format(name=name, type="int" if func == "randrange" else "float") for name, (func, _, _) in params.items())), docstring="\n".join(("        {name}: in random.{func}({args})".format(name=name, func=func, args=", ".join((map)(str, _coconut.itertools.chain.from_iterable(_coconut_reiterable(_coconut_func() for _coconut_func in (lambda: args, lambda: (k + "=" + v for k, v in kwargs.items()))))))) for name, (func, args, kwargs) in params.items())), names=", ".join(params), values="\n".join(("assert f({args}) == {loss}".format(args=", ".join((map)(str, point.values())), loss=loss) for point, loss in zip(data_points, losses))))


def get_completion_len(data_points):
    return max((len(", ".join((map)(str, point.values()))) for point in data_points)) + 1


# Backend:


class OpenAIBackend(StandardBackend):
    """OpenAI large language model BBopt backend."""
    backend_name = "openai"
    implemented_funcs = ("randrange", "uniform", "normalvariate")

    def setup_backend(self, params, engine="text-curie-001", api_key=None, debug=False):
        self.params = params

        self.engine = engine
        openai.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.debug = debug

        self.data_points = []
        self.losses = []


    def tell_data(self, new_data, new_losses):
        self.data_points += new_data
        self.losses += new_losses


    def get_next_values(self):
        prompt = get_prompt(self.params, self.data_points, self.losses)
        if self.debug:
            print("== OPENAI API PROMPT ==\n" + prompt)
        response = openai.Completion.create(engine=self.engine, prompt=prompt, max_tokens=get_completion_len(self.data_points))
        try:
            completion = response["choices"][0]["text"]
            if self.debug:
                print("== COMPLETION ==\n" + completion)
            valstr = completion.split(")", 1)[0].strip()
            values = literal_eval("(" + valstr + ",)")
            assert all((param_processor.in_support(name, val, func, *args, **kwargs) for val, (name, (func, args, kwargs)) in zip(values, self.params.items())))
        except Exception:
            raise IOError("OpenAI API call failed with response: " + repr(response))
        finally:
            if self.debug:
                print("== END ==")
        return values


# Registered names:


_coconut_call_set_names(OpenAIBackend)
OpenAIBackend.register()
OpenAIBackend.register_alg("openai")
