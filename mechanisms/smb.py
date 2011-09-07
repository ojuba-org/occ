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
import os, os.path
import re

from OjubaControlCenter.mechanismClass import mechanismClass
class OccMechanism(mechanismClass):
  smb_conf='/etc/samba/smb.conf'
  smb_global_re=re.compile(r'''^(\s*\[global\])''', re.M)
  ushare_rm_re=re.compile(r'''^(\s*\[global\][^\[]*)^\s*(?:usershare[ \t]+([^=\n]+)[ \t]*=[ \t]*([^\n]*))\s*$''',re.M | re.S)

  def __init__(self):
    mechanismClass.__init__(self,'smb')

  def __enable_ushare(self):
    self.__disable_ushare()
    t=open(self.smb_conf,'rt+').read()
    ushare="""
	usershare path = /var/lib/samba/usershare
	usershare max shares = 100
	usershare allow guests = yes
	usershare owner only = no
"""
    t,n=self.smb_global_re.subn(r'\1'+ushare,t)
    # if no global section add it
    if n==0:
      t+='\n[global]'+ushare
    ushare_path='/var/lib/samba/usershare'
    if not os.path.exists(ushare_path):
      try: os.makedirs(ushare_path)
      except OSError: pass
    try: os.chmod(ushare_path, 01777)
    except OSError: pass
    open(self.smb_conf,'wt+').write(t)
    os.system("su -l -c 'service smb restart'")
    return '0'

  def __disable_ushare(self):
    t=open(self.smb_conf,'rt+').read()
    n=1
    while(n): t,n=self.ushare_rm_re.subn(r'\1',t)
    open(self.smb_conf,'wt+').write(t)
    return '0'
  
  def enable_ushare(self, b):
    if b=='1': return self.__enable_ushare()
    return self.__disable_ushare()

  def start_on_boot(self):
    return str(os.system("su -l -c 'chkconfig --level 345 smb on'"))


