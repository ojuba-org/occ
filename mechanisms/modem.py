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
from OjubaControlCenter.mechanismClass import mechanismClass

class OccMechanism(mechanismClass):
  sl_interface_re=re.compile(r'^\s*(INTERFACE)\s*=\s*(\S*)\s*$', re.M)
  def __init__(self):
    mechanismClass.__init__(self,'modem')

  def set_sl_interface(self, i):
    try: t=open('/etc/sysconfig/slmodem','rt').read()
    except IOError: return '1'
    t,n=self.onboot_re.subn(r'\1='+i ,t)
    if n==0:
      t+="\INTERFACE=%s\n" % i
    open('/etc/sysconfig/slmodem','wt+').write(t)
    return '0'

