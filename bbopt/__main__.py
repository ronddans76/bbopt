#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x1853cc2

# Compiled with Coconut version 1.4.0-post_dev8 [Ernest Scribbler]

"""
BBopt command line interface.
"""

# Coconut Header: -------------------------------------------------------------

from __future__ import print_function, absolute_import, unicode_literals, division
import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.abspath(__file__))
_coconut_cached_module = _coconut_sys.modules.get(str("__coconut__"))
if _coconut_cached_module is not None and _coconut_os_path.dirname(_coconut_cached_module.__file__) != _coconut_file_path:
    del _coconut_sys.modules[str("__coconut__")]
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import _coconut, _coconut_MatchError, _coconut_igetitem, _coconut_base_compose, _coconut_forward_compose, _coconut_back_compose, _coconut_forward_star_compose, _coconut_back_star_compose, _coconut_pipe, _coconut_star_pipe, _coconut_back_pipe, _coconut_back_star_pipe, _coconut_bool_and, _coconut_bool_or, _coconut_none_coalesce, _coconut_minus, _coconut_map, _coconut_partial, _coconut_get_function_match_error, _coconut_addpattern, _coconut_sentinel
from __coconut__ import *
_coconut_sys.path.pop(0)

# Compiled Coconut: -----------------------------------------------------------



import os
import argparse
import subprocess
from concurrent.futures import ProcessPoolExecutor
from pprint import pprint

from bbopt.optimizer import BlackBoxOptimizer
from bbopt.constants import description
from bbopt.constants import default_trials
from bbopt.constants import default_jobs


parser = argparse.ArgumentParser(prog="bbopt", description=description)

parser.add_argument("file", metavar="file", type=str, help="path to the Python file to run")

parser.add_argument("-n", "--num-trials", metavar="trials", type=int, default=default_trials, help="number of trials to run (defaults to {})".format(default_trials))

parser.add_argument("-j", "--jobs", metavar="processes", type=int, default=default_jobs, help="number of processes to use (defaults to {})".format(default_jobs))

parser.add_argument("-q", "--quiet", action="store_true", help="suppress all informational output")

parser.add_argument("--python", metavar="executable", type=str, default="python", help="the python executable to use (defaults to 'python')")

parser.add_argument("--args", type=str, nargs=argparse.REMAINDER, help="arguments to pass to the file being run")


def base_show(quiet, msg):
    """Show the given message with [BBopt] if not quiet."""
    if not quiet:
        print("[BBopt]", msg)


def run_trial(args, cmd, i):
    """Pickleable function for running trials in parallel."""
    show = _coconut.functools.partial(base_show, args.quiet)
    show("{}/{} starting...".format(i + 1, args.num_trials))
    subprocess.check_call(cmd)
    show("{}/{} finished.".format(i + 1, args.num_trials))


def main():
    args = parser.parse_args()
    if not os.path.isfile(args.file):
        raise ValueError("could not find file {}".format(args.file))

    show = _coconut.functools.partial(base_show, args.quiet)
    cmd = [args.python, args.file] + ((lambda _coconut_none_coalesce_item: [] if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(args.args))

    show("Running {} trials using {} process(es) of:\n\t> {}".format(args.num_trials, args.jobs, " ".join(cmd)))

    if args.jobs == 1:
        for i in range(args.num_trials):
            run_trial(args, cmd, i)
    else:
        with ProcessPoolExecutor(args.jobs) as executor:
            for i in range(args.num_trials):
                executor.submit(run_trial, args, cmd, i)

    bb = BlackBoxOptimizer(args.file)
    show("Black box optimization finished; data saved to {}.".format(os.path.relpath(bb.data_file)))

    if not args.quiet:
        best_example = bb.get_optimal_run()
        show("Summary of best run:")
        pprint(bb.get_optimal_run())


if __name__ == "__main__":
    main()
