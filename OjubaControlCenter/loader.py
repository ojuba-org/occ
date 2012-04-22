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

import imp
import os
import sys
from glob import glob

def loadPlugins(pluginsDir,baseClass, pluginClassName='occPlugin', skip=[], debug=False, *args):
  # Make sure pluginsDir is in the system path so imputil works.
  if not pluginsDir in sys.path:
    sys.path.append(pluginsDir)
  pluginsList = []

  # python files list with extention stripped
  lst = map(lambda x: os.path.splitext(os.path.basename(x))[0], glob(os.path.join(pluginsDir, "*.py")))
  for module in lst:
    #print module
    # Attempt to load the found module.
    if module in skip: continue
    e=''
    try:
      f, fn, d = imp.find_module(module,[pluginsDir])
      if not fn.startswith(pluginsDir): continue
      loaded = imp.load_module(module, f, fn, d)
      f.close()
      if loaded.__dict__.has_key(pluginClassName): obj = loaded.__dict__[pluginClassName](*args)
      else: continue
    except Exception as e: e=e
    if e and debug: raise
    elif e: print "Error: %s: %s" %(module,e); continue # FIXME: reconsider this should it be continue/raise
    if not isinstance(obj, baseClass): continue
    pluginsList.append(obj)
  return pluginsList

