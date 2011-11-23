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
import re
import os
import commands
import os.path
from OjubaControlCenter.mechanismClass import mechanismClass
from OjubaControlCenter.utils import get_mounts


class OccMechanism(mechanismClass):
  def __init__(self):
    mechanismClass.__init__(self,'grub2')

  def update_grub(self):
    return commands.getstatusoutput('su -l -c "grub2-mkconfig -o /boot/grub2/grub.cfg"')
    
  def os_prober_cb(self):
    other_os_re=re.compile(r"""Found\s*.*on.*""")
    cmdstat,cmdstr=self.update_grub()
    if cmdstat:
      r="Error: %d" %cmdstat
    else:
      r="\n".join(other_os_re.findall(cmdstr))
    return r
    
  def apply_cfg(self, fn,t):
    self.write_file(fn, t)
    cmdstat,cmdstr=self.update_grub()
    if cmdstat:
      r="Error: %d" %cmdstat
    else:
      r=str(cmdstat)
    return r
    
  def write_file(self, fn, t):
    try: os.makedirs(os.path.dirname(fn))
    except OSError: pass
    open(fn, 'w+').write(t)
    
  def read_file(self, fn):
    try: return open(fn, 'r').read().strip()
    except IOError: return ''
    


