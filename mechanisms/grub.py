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
    mechanismClass.__init__(self,'gr')

  def _replace_old_items(self, cfg_fn, new_items):
    old_items_re=re.compile(r'''#Start OCC items\n(.*)\n#End OCC items''', re.S | re.M)
    grub_cont=self._read_cfg(cfg_fn)
    l,n=old_items_re.subn(new_items, grub_cont)
    if n: self._write_cfg(cfg_fn, l)
    else: self._write_cfg(cfg_fn, new_items)

  def _write_cfg(self, fn, l):
    try: os.makedirs(os.path.dirname(fn))
    except OSError: pass
    open(fn, 'w+').write(l)

  def _read_cfg(self, cfg_fn):
    try: return open(cfg_fn,'r').read().strip()
    except IOError: return ''
    
  def _to_grub_dev(self, d):
    l=re.findall('([a-z])([0-9]+)$', d)
    if not l: return None
    l,n=l[0]
    return '(hd%d,%d)' % (ord(l)-97, int(n)-1)

  def _guess_title(self, p):
    t="".join(open(os.path.join(p,'etc/issue'), 'r').read().strip().split('\n')[:1]).strip()
    #t=re.sub("[^\w \-]", "", t) # just keep alphanum and -
    return t
  
  def _detect_oses(self):
    oses=[]
    by_mnt, by_dev=get_mounts(dev_filter=lambda d: d.startswith('/dev/'), mnt_filter=lambda m: m!='/')
    for d,p in by_dev.items():
      if os.path.exists(os.path.join(p,'ntldr')):
        oses.append({"title":"Windows XP", "dev": self._to_grub_dev(d), "boot":"chainloader /ntldr"})
      elif os.path.exists(os.path.join(p,'bootmgr')):
        oses.append({"title":"Windows 7 or Vista", "dev": self._to_grub_dev(d), "boot":"chainloader /bootmgr"})
      elif os.path.exists(os.path.join(p,'boot/grub/grub.conf')):
        oses.append({"title":self._guess_title(p), "dev": self._to_grub_dev(d), "boot":"configfile /boot/grub/grub.conf"})
      elif os.path.exists(os.path.join(p,'grub/grub.conf')):
        oses.append({"title":"Linux Generic", "dev": self._to_grub_dev(d), "boot":"configfile /grub/grub.conf"})
      elif os.path.exists(os.path.join(p,'boot/grub/core.img')):
        oses.append({"title":self._guess_title(p), "dev": self._to_grub_dev(d), "boot":"chainloader /boot/grub/core.img"})
      elif os.path.exists(os.path.join(p,'grub/core.img')):
        oses.append({"title":"Linux Generic", "dev": self._to_grub_dev(d), "boot":"chainloader /grub/core.img"})
    return oses

  def set_grub_items(self):
    cfg_fn='/boot/grub/grub.conf'
    t='''
title %(title)s
rootnoverify %(dev)s
%(boot)s
'''
    os_ls=self._detect_oses()
    items=map(lambda d: t % d, os_ls)
    new_items='\n#Start OCC items\n%s\n#End OCC items' % '\n'.join(items)
    r=self._replace_old_items(cfg_fn, new_items)
    return str(len(os_ls))
  

