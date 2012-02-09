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

import os.path
import re
from OjubaControlCenter.mechanismClass import mechanismClass

class OccMechanism(mechanismClass):
  gdm_conf="/etc/gdm/custom.conf"
  kdm_conf="/etc/kde/kdm/kdmrc"
  lxdm_conf="/etc/lxdm/lxdm.conf"
  dm_re=re.compile(r'''^\s*DISPLAYMANAGER\s*=\s*['"]?([^'"]+)['"]?\s*$''',re.M)
  gdm_daemon_re=re.compile(r'''^(\s*\[daemon\])''', re.M)
  gdm_re=re.compile(r'''^(\s*\[daemon\][^\[]*)^\s*(AutomaticLoginEnable[ \t]*=[ \t]*([^\n]*))\s*$''',re.M | re.S)
  gdm_user_re=re.compile(r'''^(\s*\[daemon\][^\[]*)^\s*(AutomaticLogin[ \t]*=[ \t]*([^\n]*))\s*$''',re.M | re.S)
  gdm_clean_re=re.compile(r'''^(\s*\[daemon\][^\[]*)^\s*((TimedLoginEnable|TimedLogin|TimedLoginDelay)[ \t]*=[ \t]*([^\n]*))\s*$''',re.M | re.S)
  kdm_core_re=re.compile(r'''^(\s*\[X-:0-Core\])''', re.M)
  kdm_re=re.compile(r'''^(\s*\[X-:0-Core\][^\[]*)^\s*(AutoLoginEnable[ \t]*=[ \t]*([^\n]*))\s*$''',re.M | re.S)
  kdm_user_re=re.compile(r'''^(\s*\[X-:0-Core\][^\[]*)^\s*(AutoLoginUser[ \t]*=[ \t]*([^\n]*))\s*$''',re.M | re.S)
  lxdm_re=re.compile(r'''^(\s*\[base\][^\[]*)^#?\s*(autologin[ \t]*=[ \t]*([^\n]*))?\s*$''',re.M | re.S)
  lxdm_clean_re=re.compile(r'''^\s*(autologin[ \t]*=[ \t]*([^\n]*))\s*$''',re.M | re.S)

  def __init__(self):
    mechanismClass.__init__(self,'dm')

  def __get_current(self):
    v=''
    if os.path.exists("/etc/sysconfig/desktop"):
      try: l=open("/etc/sysconfig/desktop","rt").read()
      except IOError: v=''
      else:
        try: v=self.dm_re.findall(l)[-1].strip()
        except IndexError: v=''
    if not v:
      if os.path.exists("/usr/sbin/gdm") or os.path.exists("/usr/bin/gdm"): v='gdm'
      elif os.path.exists("/usr/bin/kdm") or os.path.exists("/usr/sbin/kdm"): v='kdm'
      else: return ''
    v=v.lower()
    if v=='gnome': v='gdm'
    elif v=='kde': v='kdm'
    v=v.split('/')[-1]
    return v

  def lxdm_autologin(self, u):
    t=open(self.lxdm_conf,'rt').read()
    t,n=self.lxdm_re.subn(r'\1autologin=%s'%u,t)
    if n==0: return False
    open(self.lxdm_conf,'wt+').write(t)
    return True
    
  def lxdm_disable_autologin(self):
    t=open(self.lxdm_conf,'rt').read()
    n=1
    while(n): t,n=self.lxdm_clean_re.subn(r'# \1',t)
    open(self.lxdm_conf,'wt+').write(t)
    return True
    
  def __gdm_autologin(self, u):
    self.__gdm_disable_autologin()
    t=open(self.gdm_conf,'rt').read()
    # instead of modifying the lines if they exists
    #t,n=gdm_re.subn(r'\1AutomaticLoginEnable=true',t)
    #t,n=gdm_user_re.subn(r'\1AutomaticLogin='+u,t)

    # I'm going to remove them then add the new values
    t,n=self.gdm_daemon_re.subn(r'\1\nAutomaticLoginEnable=true\nAutomaticLogin=%s\n' % u,t)
    # if no daemon section add it
    if n==0:
      t+='\n[daemon]\nAutomaticLoginEnable=true\nAutomaticLogin=%s\n' % u
    open(self.gdm_conf,'wt+').write(t)
    return True

  def __gdm_disable_autologin(self):
    t=open(self.gdm_conf,'rt').read()
    n=1
    while(n): t,n=self.gdm_re.subn(r'\1',t)
    n=1
    while(n): t,n=self.gdm_user_re.subn(r'\1',t)
    # disable timedlogin
    n=1
    while(n): t,n=self.gdm_clean_re.subn(r'\1',t)
    open(self.gdm_conf,'wt+').write(t)
    return True

  def __kdm_autologin(self, u):
    t=open(self.kdm_conf,'rt').read()
    t,n=self.kdm_re.subn(r'\1AutoLoginEnable=true',t)
    if n==0:
      t,n=self.kdm_core_re.subn(r'\1AutoLoginEnable=true',t)
      if n==0: return False # could not find core section
    t,n=self.kdm_user_re.subn(r'\1AutoLoginUser='+u,t)
    if n==0:
      t,n=self.kdm_core_re.subn(r'\1\nAutoLoginUser=%s\n' % u,t)
      if n==0: return False # could not find core section
    open(self.kdm_conf,'wt+').write(t)
    return True

  def __kdm_disable_autologin(self):
    t=open(self.kdm_conf,'rt').read()
    n=1
    while(n): t,n=self.kdm_re.subn(r'\1',t)
    n=1
    while(n): t,n=self.kdm_user_re.subn(r'\1',t)
    open(self.kdm_conf,'wt+').write(t)
    return True


  def enable_autologin(self, u):
    dm=self.__get_current()
    if not dm: return ''
    if dm=='gdm' and self.__gdm_autologin(u): return dm
    elif dm=='kdm' and self.__kdm_autologin(u): return dm
    elif dm=='lxdm' and self.lxdm_autologin(u): return dm
    return '-'+dm

  def disable_autologin(self):
    dm=self.__get_current()
    if not dm: return ''
    if dm=='gdm' and self.__gdm_disable_autologin(): return dm
    elif dm=='kdm' and self.__kdm_disable_autologin(): return dm
    elif dm=='lxdm' and self.lxdm_disable_autologin(): return dm
    return '-'+dm

