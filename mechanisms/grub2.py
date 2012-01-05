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

import os
import re
from OjubaControlCenter.utils import cmd_out, copyfile
from OjubaControlCenter.mechanismClass import mechanismClass
from OjubaControlCenter.utils import get_mounts


class OccMechanism(mechanismClass):
  def __init__(self):
    mechanismClass.__init__(self,'grub2')
  
  def update_grub(self):
    return cmd_out('su -l -c "grub2-mkconfig -o /boot/grub2/grub.cfg"')
    
  def os_prober_cb(self):
    other_os_re=re.compile(r"""Found\s*.*on.*""")
    cmdout,cmderr=self.update_grub()
    if cmdout: r="Error: %d" %cmdstat
    else: r="\n".join(other_os_re.findall(cmderr))
    return r
    
  def apply_cfg(self, fn, t, font, pic):
    old_t=self.read_file(fn)
    bg='/boot/grub2/oj.grub2.png'
    if not self.write_file(fn, t):
      self.write_file(fn, old_t)
      return "Error: Cant not write config file"
    try: copyfile(pic, bg)
    except IOError: pass
    if font and os.path.isfile(font): 
      cmd_out('su -l -c "grub2-mkfont --output=/boot/grub2/unicode.pf2 %s"'%font)
    else: 
      if os.path.isfile('/boot/grub2/unicode.pf2'): os.unlink('/boot/grub2/unicode.pf2')
    cmdout,cmderr=self.update_grub()
    if cmdout: r="Error: %d" %cmderr
    else: r='0'
    return r
    
  def write_file(self, fn, t):
    try: os.makedirs(os.path.dirname(fn))
    except OSError: pass
    try: open(fn, 'w+').write(t)
    except UnicodeEncodeError: return False
    except IOError: return False
    return True
    
  def read_file(self, fn):
    try: return open(fn, 'r').read().strip()
    except IOError: return ''
    except UnicodeEncodeError: return ''
    


