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

import ihooks, imp, py_compile
import os, sys
from glob import glob

class occHooks(ihooks.Hooks):
    """ emulate python import """
    def load_source(self, name, filename, file=None):
        """Compile source files with any line ending."""
        if file:
            file.close()
        py_compile.compile(filename)    # line ending conversion is in here
        cfile = open(filename + (__debug__ and 'c' or 'o'), 'rb')
        try:
            return self.load_compiled(name, filename, cfile)
        finally:
            cfile.close()

class Loader(object):
    # TODO: add more doc details
    """ load modules """
    def __init__(self, pluginsDir, baseClass, pluginClassName='occPlugin', skip=[], debug=False, *args):
        self.pluginsDir = pluginsDir
        self.baseClass = baseClass
        self.pluginClassName = pluginClassName
        self.skip = skip
        self.debug = debug
        self.args = args
        self.loaded_plugins = {}
        if not self.pluginsDir in sys.path:
            sys.path.append(self.pluginsDir)
        
    def get_plugins(self):
        hook = occHooks()
        pluginsList = []
        # python files list with extention stripped
        lst = map(lambda x: os.path.splitext(os.path.basename(x))[0],
                            glob(os.path.join(self.pluginsDir, "*.py")))
        for module in lst:
            m = hook.load_source(module, os.path.join(self.pluginsDir, module + '.py'))
            
            valid_plugin = m.__dict__.has_key(self.pluginClassName) and \
                           m.__dict__.has_key('category') and \
                           m.__dict__.has_key('caption') and \
                           m.__dict__.has_key('description') and \
                           m.__dict__.has_key('priority')
                           
            if valid_plugin:
                obj = {'name': module,
                       'category': m.__dict__['category'],
                       'caption': m.__dict__['caption'],
                       'description': m.__dict__['description'],
                       'priority': m.__dict__['priority'], }
                pluginsList.append(obj)
        return pluginsList
      
    def load_plugin(self, module):
        if type(module) == dict:
            if 'name' in module :
                module = module['name']

        if module in self.skip:
            return []
        # the module loaded, don't load aother instance
        if module in self.loaded_plugins:
            return [True, self.loaded_plugins[module]]
        
        # load module
        e = ''
        f, fn, d = imp.find_module(module, [self.pluginsDir])
        try:
            
            if not fn.startswith(self.pluginsDir): return []
            loaded = imp.load_module(module, f, fn, d)
            if loaded.__dict__.has_key(self.pluginClassName):
                obj = loaded.__dict__[self.pluginClassName](*self.args)
            else:
                return []
        except Exception as e: e=e
        finally: f.close()
        
        # if import errors
        if e and self.debug: raise
        elif e: print "Error: %s: %s" %(module,e); return []
        
        #if not isinstance(obj, self.baseClass):
            #print self.baseClass, obj.__dict__
            #return None
        # add succeeded imports to loaded plugins
        self.loaded_plugins[module] = obj
        # return packe stat( False for new plugins ), loaded object
        return [False, obj]

