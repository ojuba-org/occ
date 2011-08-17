# -*- coding: utf-8 -*-
"""
Ojuba Control Center
Copyright © 2009, Muayyad Alsadi <alsadi@ojuba.org>

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
import os
import os.path
from OjubaControlCenter.utils import *
from OjubaControlCenter.mechanismClass import mechanismClass
class OccMechanism(mechanismClass):
  def __init__(self):
    mechanismClass.__init__(self,'run')

  def in_bg(self,cmd):
    run_in_bg("su -l -c '%s'" % cmd)
    return '0'

  def system(self,cmd):
    return str(os.system("su -l -c '%s'" % cmd))

  def fileman(self,p):
    run_in_bg("su -l -c '%s'" % file_man_cmd(p))
    return '0'
  
  def write_conf(self, fn, cont):
    open(fn, 'wt+').write(cont)
    return '0'
