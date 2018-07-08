#!/usr/bin/env python3
# coding: utf-8

import sys
import ctypes
from ctypes import c_uint32, c_char_p

prefix = {'win32': ''}.get(sys.platform, 'lib')
extension = {'darwin': '.dylib', 'win32': '.dll'}.get(sys.platform, '.so')
lib = ctypes.cdll.LoadLibrary(prefix + "string_arguments" + extension)

lib.fromPy.argtypes = (c_char_p,)
lib.fromPy.restype = c_uint32

print(lib.how_many_characters("göes to élevên".encode('utf-8')))

# if name == "__main__":
