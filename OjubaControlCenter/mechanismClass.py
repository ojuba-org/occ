# -*- coding: utf-8 -*-
"""
Ojuba Control Center
Copyright © 2009, Ojuba Team <core@ojuba.org>

    Released under terms of Waqf Public License.
    This program is free software; you can redistribute it and/or modify
    it under the terms of the latest version Waqf Public License as
    published by Ojuba.org.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

    The Latest version of the license can be found on
    "http://waqf.ojuba.org/license"
"""
class mechanismClass(object):
  def __init__(self, name):
    self.name=name
  def call(self, *args):
    if len(args)<1: return ''
    o,a=args[0],args[1:]
    if o.startswith('__'): return '' # don't call internal methods
    # add try except when end with teasting
    return self.__getattribute__(o)(*a)
    return ''
