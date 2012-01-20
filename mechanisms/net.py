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
from OjubaControlCenter.mechanismClass import mechanismClass

class OccMechanism(mechanismClass):
  onboot_re=re.compile(r'^\s*(ONBOOT)\s*=\s*(\S*)\s*$', re.M)
  nm_ctl_re=re.compile(r'^\s*(NM_CONTROLLED)\s*=\s*(\S*)\s*$', re.M)
  usr_ctl_re=re.compile(r'^\s*(USERCTL)\s*=\s*(\S*)\s*$', re.M)
  def __init__(self):
    mechanismClass.__init__(self,'net')

  def set_nm_service(self):
    os.system("su -l -c 'chkconfig --level 12345 network off'")
    r=str(os.system("su -l -c 'chkconfig --level 345 NetworkManager on'"))
    os.system("su -l -c 'service network stop; service NetworkManager restart'")
    return r

  def nic_set_onboot(self, nic):
    t=open(nic,'rt+').read()
    t,n=self.onboot_re.subn(r'\1=yes',t)
    if n==0:
      t+="\nONBOOT=yes\n"
    open(nic,'wt+').write(t)
    return '0'

  def nic_set_nm(self, nic):
    t=open(nic,'rt+').read()
    t,n=self.nm_ctl_re.subn(r'\1=yes',t)
    if n==0:
      t+="\nNM_CONTROLLED=yes\n"
    open(nic,'wt+').write(t)
    return '0'

  def nic_set_userctl(self, nic):
    t=open(nic,'rt+').read()
    t,n=self.usr_ctl_re.subn(r'\1=yes',t)
    print n
    if n==0:
      t+="\nUSERCTL=yes\n"
    open(nic,'wt+').write(t)
    return '0'

