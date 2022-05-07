#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x5635d7dc

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



import os  #5 (line num in coconut source)
from ast import literal_eval  #6 (line num in coconut source)

import openai  #8 (line num in coconut source)

from bbopt import constants  #10 (line num in coconut source)
from bbopt.util import printerr  #11 (line num in coconut source)
from bbopt.util import mean_abs_dev  #11 (line num in coconut source)
from bbopt.util import mean  #11 (line num in coconut source)
from bbopt.params import param_processor  #12 (line num in coconut source)
from bbopt.backends.util import StandardBackend  #13 (line num in coconut source)
from bbopt.backends.util import sorted_params  #13 (line num in coconut source)


# Utilities:

def get_prompt(params, data_points, losses, hoped_for_loss):  #18 (line num in coconut source)
    """Get the base OpenAI API prompt."""  #19 (line num in coconut source)
    return '''# black box function to be minimized
def f({func_params}) -> float:
    """
    parameters:
{docstring}

    returns:
        float: the loss
    """
    return black_box_loss({names})

# experimentally observed data
# new experiments MUST stay within the bounds, SHOULD fully explore the bounds, and SHOULD converge to minimum
# bounds: f({bounds})
{values}{hoped_for_loss} == f('''.format(func_params=", ".join(("{name}: {type}".format(name=name, type=("int" if func == "randrange" else type(args[0][0]).__name__ if func == "choice" and all_equal(map(type, args[0])) else "typing.Any" if func == "choice" else "float")) for name, (func, args, _) in params.items())), docstring="\n".join(("        {name}: in {func}({args})".format(name=name, func="range" if func == "randrange" else func, args=", ".join((map)(repr, (args[:2] if func == "randrange" and args[-1] == 1 else args)))) for name, (func, args, _) in params.items())), names=", ".join(params), bounds=", ".join(("{name}: {func}({args})".format(name=name, func="range" if func == "randrange" else func, args=", ".join((map)(repr, (args[:2] if func == "randrange" and args[-1] == 1 else args)))) for name, (func, args, _) in params.items())), values="".join(("{loss} == f({named_args})\n".format(named_args=", ".join((map)(lambda name: "{_coconut_format_0}={_coconut_format_1!r}".format(_coconut_format_0=(name), _coconut_format_1=(point[name])), params)), loss=loss) for point, loss in zip(data_points, losses))), hoped_for_loss=int(hoped_for_loss) if int(hoped_for_loss) == hoped_for_loss else hoped_for_loss)  #34 (line num in coconut source)



def is_int(x):  #75 (line num in coconut source)
    return int(x) == x  #75 (line num in coconut source)



def typed(average):  #78 (line num in coconut source)
    """Get a typed version of average."""  #79 (line num in coconut source)
    def typed_average(xs):  #80 (line num in coconut source)
        xs = tuple(xs)  #82 (line num in coconut source)
        mu = mean(xs)  #83 (line num in coconut source)
        return int(round(mu)) if all((map)(is_int, xs)) else mu  #84 (line num in coconut source)

    return typed_average  #84 (line num in coconut source)



def get_loss_eps(typical_loss):  #87 (line num in coconut source)
    """Get a reasonably-sized hoped for loss improvement."""  #88 (line num in coconut source)
    a, b = float(abs(typical_loss)).as_integer_ratio()  #89 (line num in coconut source)
    little_a = int("1" * len(str(a)))  #90 (line num in coconut source)
    return little_a / b  #91 (line num in coconut source)


# Backend:


class OpenAIBackend(StandardBackend):  #96 (line num in coconut source)
    """OpenAI large language model BBopt backend."""  #97 (line num in coconut source)
    backend_name = "openai"  #98 (line num in coconut source)
    implemented_funcs = ("randrange", "uniform", "normalvariate", "choice")  #99 (line num in coconut source)

    max_prompt_len = float("inf")  #106 (line num in coconut source)

    def setup_backend(self, params, engine=None, temperature=None, max_retries=None, api_key=None, debug=False):  #108 (line num in coconut source)
        self.params = sorted_params(params)  #109 (line num in coconut source)

        self.engine = (constants.openai_default_engine if engine is None else engine)  #111 (line num in coconut source)
        self.temp = (constants.openai_default_temp if temperature is None else temperature)  #112 (line num in coconut source)
        self.max_retries = (lambda _coconut_x: constants.openai_default_max_retries if _coconut_x is None else _coconut_x)(max_retries)  #113 (line num in coconut source)
        openai.api_key = (lambda _coconut_x: os.getenv("OPENAI_API_KEY") if _coconut_x is None else _coconut_x)(api_key)  #114 (line num in coconut source)
        self.debug = debug  #115 (line num in coconut source)

        self.data_points = []  #117 (line num in coconut source)
        self.losses = []  #118 (line num in coconut source)
        self.cached_values = ()  #119 (line num in coconut source)


    def tell_data(self, new_data, new_losses):  #121 (line num in coconut source)
        for point, loss in zip(new_data, new_losses):  #122 (line num in coconut source)
# avoid (point, loss) duplicates since they cause GPT to repeat itself
            try:  #124 (line num in coconut source)
                existing_index = self.data_points.index(point)  #125 (line num in coconut source)
            except ValueError:  #126 (line num in coconut source)
                existing_index = None  #127 (line num in coconut source)
            if existing_index is None or self.losses[existing_index] != loss:  #128 (line num in coconut source)
                self.data_points.append(point)  #129 (line num in coconut source)
                self.losses.append(loss)  #130 (line num in coconut source)


    def get_prompt(self):  #132 (line num in coconut source)
        """Get the OpenAI API prompt to use."""  #133 (line num in coconut source)
        return (get_prompt(self.params, self.data_points, self.losses, hoped_for_loss=min(self.losses) - (typed(mean_abs_dev))(self.losses) - get_loss_eps((typed(mean))(self.losses))) + ", ".join((starmap)(lambda name, vals: "{_coconut_format_0}={_coconut_format_1!r}".format(_coconut_format_0=(name), _coconut_format_1=(vals)), zip(self.params, self.cached_values))) + ("," if self.cached_values else ""))  #134 (line num in coconut source)


    @property  #147 (line num in coconut source)
    def expected_params(self):  #148 (line num in coconut source)
        """The parameters that are expected to be in the prompt."""  #149 (line num in coconut source)
        return _coconut_iter_getitem(self.params.keys(), _coconut.slice(len(self.cached_values), None))  #150 (line num in coconut source)


    def get_completion_len(self):  #152 (line num in coconut source)
        """Get the maximum number of characters in a completion."""  #153 (line num in coconut source)
        return max((len(", ".join(", ".join((map)(lambda name: "{_coconut_format_0}={_coconut_format_1!r}".format(_coconut_format_0=(name), _coconut_format_1=(point[name])), self.expected_params)))) for point in self.data_points)) + 1  #154 (line num in coconut source)


    def to_python(self, completion):  #159 (line num in coconut source)
        """Convert a completion to Python code as best as possible."""  #160 (line num in coconut source)
        completion = completion.strip(",")  #161 (line num in coconut source)
        for repl, to in _coconut.itertools.chain.from_iterable(_coconut_reiterable(_coconut_func() for _coconut_func in (lambda: (("\u2212", "-"), ("\u2018", "'"), ("\u2019", "'"), ("\u201c", '"'), ("\u201d", '"'), ("\u221e", 'float("inf")')), lambda: (("{_coconut_format_0}:".format(_coconut_format_0=(name)), "{name}=") for name in self.params)))):  #162 (line num in coconut source)
            completion = completion.replace(repl, to)  #172 (line num in coconut source)

# treat as dictionary
        if all(("{_coconut_format_0}=".format(_coconut_format_0=(name)) in completion for name in self.expected_params)):  #175 (line num in coconut source)
            for name in self.expected_params:  #176 (line num in coconut source)
                completion = completion.replace("{_coconut_format_0}=".format(_coconut_format_0=(name)), '"{_coconut_format_0}":'.format(_coconut_format_0=(name)))  #177 (line num in coconut source)
            completion = "{" + completion + "}"  #178 (line num in coconut source)
            if self.debug:  #179 (line num in coconut source)
                print("== PYTHON ==\n" + completion)  #180 (line num in coconut source)
            valdict = literal_eval(completion)  #181 (line num in coconut source)
            return tuple((valdict[name] for name in self.expected_params))  #182 (line num in coconut source)

# treat as tuple
        else:  #185 (line num in coconut source)
            for name in self.params:  #186 (line num in coconut source)
                completion = completion.replace("{_coconut_format_0}=".format(_coconut_format_0=(name)), "")  #187 (line num in coconut source)
            completion = "(" + completion + ",)"  #188 (line num in coconut source)
            if self.debug:  #189 (line num in coconut source)
                print("== PYTHON ==\n" + completion)  #190 (line num in coconut source)
            return literal_eval(completion)  #191 (line num in coconut source)


    def get_next_values(self):  #193 (line num in coconut source)
# generate prompt
        prompt = self.get_prompt()  #195 (line num in coconut source)
        while len(prompt) > self.max_prompt_len:  #196 (line num in coconut source)
            self.data_points.pop(0)  #197 (line num in coconut source)
            self.losses.pop(0)  #198 (line num in coconut source)
            prompt = self.get_prompt()  #199 (line num in coconut source)
        if self.debug:  #200 (line num in coconut source)
            print("\n== PROMPT ==\n" + prompt)  #201 (line num in coconut source)

# query api
        try:  #204 (line num in coconut source)
            response = openai.Completion.create(engine=self.engine, prompt=prompt, temperature=self.temp, max_tokens=self.get_completion_len())  #205 (line num in coconut source)
        except openai.error.InvalidRequestError as api_err:  #211 (line num in coconut source)
            if self.debug:  #212 (line num in coconut source)
                print("== END ==")  #213 (line num in coconut source)
            if not str(api_err).startswith(constants.openai_max_context_err_prefix):  #214 (line num in coconut source)
                raise  #215 (line num in coconut source)
            if self.debug:  #216 (line num in coconut source)
                print("ERROR: got max context length error with self.max_prompt_len={_coconut_format_0}".format(_coconut_format_0=(self.max_prompt_len)))  #217 (line num in coconut source)
            if self.max_prompt_len == float("inf"):  #218 (line num in coconut source)
                self.max_prompt_len = len(prompt.rsplit("\n", 1)[0])  #219 (line num in coconut source)
            else:  #220 (line num in coconut source)
                self.max_prompt_len -= self.get_completion_len()  #221 (line num in coconut source)
            return self.retry_get_values()  #222 (line num in coconut source)

# parse response
        try:  #225 (line num in coconut source)
            completion = response["choices"][0]["text"]  #226 (line num in coconut source)
            if self.debug:  #227 (line num in coconut source)
                print("== COMPLETION ==\n" + completion)  #228 (line num in coconut source)
            valvec = self.to_python(completion.split(")", 1)[0].strip())  #229 (line num in coconut source)
        except BaseException as parse_err:  #230 (line num in coconut source)
            if self.debug:  #231 (line num in coconut source)
                print("== END ==")  #232 (line num in coconut source)
            if self.debug:  #233 (line num in coconut source)
                print("ERROR: {_coconut_format_0} for API response:\n{_coconut_format_1}".format(_coconut_format_0=(parse_err), _coconut_format_1=(response)))  #234 (line num in coconut source)
            return self.retry_get_values(temp=(self.temp + constants.openai_default_temp) / 2)  #235 (line num in coconut source)
        if self.debug:  #236 (line num in coconut source)
            print("== END ==")  #237 (line num in coconut source)
        @_coconut_mark_as_match  #238 (line num in coconut source)
        def _coconut_lambda_0(*_coconut_match_args, **_coconut_match_kwargs):  #238 (line num in coconut source)
            _coconut_match_check_0 = False  #238 (line num in coconut source)
            _coconut_match_set_name_val = _coconut_sentinel  #238 (line num in coconut source)
            _coconut_match_set_name_name = _coconut_sentinel  #238 (line num in coconut source)
            _coconut_match_set_name_func = _coconut_sentinel  #238 (line num in coconut source)
            _coconut_match_set_name_args = _coconut_sentinel  #238 (line num in coconut source)
            _coconut_match_set_name_kwargs = _coconut_sentinel  #238 (line num in coconut source)
            _coconut_FunctionMatchError = _coconut_get_function_match_error()  #238 (line num in coconut source)
            if _coconut.len(_coconut_match_args) == 1:  #238 (line num in coconut source)
                if (_coconut.isinstance(_coconut_match_args[0], _coconut.abc.Sequence)) and (_coconut.len(_coconut_match_args[0]) == 2) and (_coconut.isinstance(_coconut_match_args[0][1], _coconut.abc.Sequence)) and (_coconut.len(_coconut_match_args[0][1]) == 2) and (_coconut.isinstance(_coconut_match_args[0][1][1], _coconut.abc.Sequence)) and (_coconut.len(_coconut_match_args[0][1][1]) == 3):  #238 (line num in coconut source)
                    _coconut_match_set_name_val = _coconut_match_args[0][0]  #238 (line num in coconut source)
                    _coconut_match_set_name_name = _coconut_match_args[0][1][0]  #238 (line num in coconut source)
                    _coconut_match_set_name_func = _coconut_match_args[0][1][1][0]  #238 (line num in coconut source)
                    _coconut_match_set_name_args = _coconut_match_args[0][1][1][1]  #238 (line num in coconut source)
                    _coconut_match_set_name_kwargs = _coconut_match_args[0][1][1][2]  #238 (line num in coconut source)
                    if not _coconut_match_kwargs:  #238 (line num in coconut source)
                        _coconut_match_check_0 = True  #238 (line num in coconut source)
            if _coconut_match_check_0:  #238 (line num in coconut source)
                if _coconut_match_set_name_val is not _coconut_sentinel:  #238 (line num in coconut source)
                    val = _coconut_match_set_name_val  #238 (line num in coconut source)
                if _coconut_match_set_name_name is not _coconut_sentinel:  #238 (line num in coconut source)
                    name = _coconut_match_set_name_name  #238 (line num in coconut source)
                if _coconut_match_set_name_func is not _coconut_sentinel:  #238 (line num in coconut source)
                    func = _coconut_match_set_name_func  #238 (line num in coconut source)
                if _coconut_match_set_name_args is not _coconut_sentinel:  #238 (line num in coconut source)
                    args = _coconut_match_set_name_args  #238 (line num in coconut source)
                if _coconut_match_set_name_kwargs is not _coconut_sentinel:  #238 (line num in coconut source)
                    kwargs = _coconut_match_set_name_kwargs  #238 (line num in coconut source)
            if not _coconut_match_check_0:  #238 (line num in coconut source)
                raise _coconut_FunctionMatchError('|> takewhile$(def ((val, (name, (func, args, kwargs)))) ->', _coconut_match_args)  #238 (line num in coconut source)
            return param_processor.in_support(name, val, func, *args, **kwargs)  #238 (line num in coconut source)
        legal_values = ((tuple)((map)(_coconut.operator.itemgetter((0)), (takewhile)(_coconut_lambda_0, (_coconut_partial(zip, {1: self.params.items()}, 2))((self.cached_values + valvec)[_coconut.slice(None, len(self.params))])))))  #238 (line num in coconut source)
        if len(legal_values) < len(self.params):  #247 (line num in coconut source)
            if self.debug:  #248 (line num in coconut source)
                if len(valvec) < len(self.params) - len(self.cached_values):  #249 (line num in coconut source)
                    print("ERROR: insufficient values (got {_coconut_format_0}; expected {_coconut_format_1})".format(_coconut_format_0=(len(valvec)), _coconut_format_1=(len(self.params) - len(self.cached_values))))  #250 (line num in coconut source)
                else:  #251 (line num in coconut source)
                    print("ERROR: got illegal values: {_coconut_format_0!r}".format(_coconut_format_0=(valvec)))  #252 (line num in coconut source)
            return self.retry_get_values(temp=(self.temp + constants.openai_default_temp) / 2, cached_values=legal_values)  #253 (line num in coconut source)

# return values
        values = dict(((name), (val)) for name, val in zip(self.params, legal_values))  #256 (line num in coconut source)
        if values in self.data_points:  #257 (line num in coconut source)
            if self.debug:  #258 (line num in coconut source)
                print("ERROR: got duplicate point: {_coconut_format_0!r}".format(_coconut_format_0=(legal_values)))  #259 (line num in coconut source)
            return self.retry_get_values(temp=self.temp + (constants.openai_max_temp - self.temp) / 2, cached_values=())  #260 (line num in coconut source)
        return values  #261 (line num in coconut source)


    def retry_get_values(self, temp=None, cached_values=None):  #263 (line num in coconut source)
        """Used in get_next_values to keep track of recursive calls."""  #264 (line num in coconut source)
        if not self.max_retries:  #265 (line num in coconut source)
            if self.debug:  #266 (line num in coconut source)
                print()  #267 (line num in coconut source)
            printerr("BBopt Warning: Maximum number of OpenAI API retries exceeded for {_coconut_format_0} on:\n== PROMPT ==\n{_coconut_format_1}\n== END ==".format(_coconut_format_0=(self.engine), _coconut_format_1=(self.get_prompt())))  #268 (line num in coconut source)
            return {}  # return empty values so that the fallback random backend will be used instead  #269 (line num in coconut source)
        if self.debug:  #270 (line num in coconut source)
            if temp is None:  #271 (line num in coconut source)
                print("RETRYING with: self.max_prompt_len={_coconut_format_0}".format(_coconut_format_0=(self.max_prompt_len)))  #272 (line num in coconut source)
            else:  #273 (line num in coconut source)
                print("RETRYING with new temperature: {_coconut_format_0} -> {_coconut_format_1}".format(_coconut_format_0=(self.temp), _coconut_format_1=(temp)))  #274 (line num in coconut source)
        old_retries, self.max_retries = self.max_retries, self.max_retries - 1  #275 (line num in coconut source)
        if temp is not None:  #276 (line num in coconut source)
            old_temp, self.temp = self.temp, temp  #277 (line num in coconut source)
        if cached_values is not None:  #278 (line num in coconut source)
            if self.debug:  #279 (line num in coconut source)
                print("CACHING values: {_coconut_format_0} -> {_coconut_format_1}".format(_coconut_format_0=(self.cached_values), _coconut_format_1=(cached_values)))  #280 (line num in coconut source)
            self.cached_values = cached_values  #281 (line num in coconut source)
        try:  #282 (line num in coconut source)
            return self.get_next_values()  #283 (line num in coconut source)
        finally:  #284 (line num in coconut source)
            self.max_retries = old_retries  #285 (line num in coconut source)
            if temp is not None:  #286 (line num in coconut source)
                self.temp = old_temp  #287 (line num in coconut source)
            if cached_values is not None:  #288 (line num in coconut source)
                self.cached_values = ()  #289 (line num in coconut source)


# Registered names:


_coconut_call_set_names(OpenAIBackend)  #294 (line num in coconut source)
OpenAIBackend.register()  #294 (line num in coconut source)
OpenAIBackend.register_alg("openai")  #295 (line num in coconut source)
OpenAIBackend.register_alg("openai_debug", debug=True)  #296 (line num in coconut source)
OpenAIBackend.register_alg("openai_davinci", engine=constants.openai_davinci_engine)  #297 (line num in coconut source)
