#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x23a4b462

# Compiled with Coconut version 1.3.0-post_dev2 [Dead Parrot]

"""
Utilities for use across all of BBGun.
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

import os.path

# Functions:

def is_str(obj):
    return isinstance(obj, (str, py_str))

def norm_path(path):
    return ((os.path.normcase)((os.path.realpath)((os.path.abspath)((os.path.expanduser)(path)))))

def encode_bytes(bytestring):
    """Encode bytes for JSON."""
    return ":".join((hex(x)[2:] for x in (bytearray)(bytestring)))

def decode_bytes(encoded):
    """Decode bytes for JSON."""
    return (bytes)(bytearray((int(x, 16) for x in encoded.split(":"))))
