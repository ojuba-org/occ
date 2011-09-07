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
class OccMechanism(mechanismClass):
  def __init__(self):
    mechanismClass.__init__(self,'gr')

  def guess_os(self, path):
    if 'ntldr' in map(lambda a: a.lower(),os.listdir(path)): return '2'
    if 'bootmgr' in map(lambda a: a.lower(),os.listdir(path)): return '3'
    if not os.path.isdir(os.path.join(path,'boot/grub/')): return None
    if 'grub.conf' in map(lambda a: a.lower(),os.listdir(os.path.join(path,'boot/grub/'))): return '0'
    if 'grub.cfg' in map(lambda a: a.lower(),os.listdir(os.path.join(path,'boot/grub/'))): return '1'
    return None

  def rm_old_items(self, cfg_fn):
    old_items_re=re.compile(r'''(\n*#Start OCC items(\n.*)*#End OCC items)\n*''')
    grub_cont=self.read_cfg(cfg_fn)
    l,e=old_items_re.subn(r'\n' ,grub_cont)
    self.write_cfg(cfg_fn, l)
    return l
    
  def write_cfg(self, fn, l):
    open(fn, 'wt+').write(l)

  def read_cfg(self, cfg_fn):
    return open(cfg_fn,'r').read().strip()
    
  def sdtohd(self, s):
      l_ls=map(chr, range(97, 123))
      ls=s.split('/')[-1]
      l=ls[2:3]
      l=l_ls.index(l)
      n=int(ls[3:])-1
      return '(hd%d,%d)' % (l,n)
      
  def setup_item(self, o, p, mp):
      title = 'Unknown OS'
      if o == 0 or o == 1:
        title=open(os.path.join(mp,'etc/issue'), 'r').read().strip().split('\n')[0]
        root='root %s' % self.sdtohd(p)
        if o == 0 : kernel = 'configfile /boot/grub/grub.conf'
        else: kernel = 'kernel /boot/grub/core.img'
      else:
        root='rootnoverify %s' % self.sdtohd(p)
        if o == 2 : kernel = 'chainloader /ntldr' ; title = 'Windows XP'
        else: kernel = 'chainloader /bootmgr' ; title = 'Windows 7/Vista'
      return title,'title %s\n  %s\n  %s\n' %(title,root,kernel)

  def find_installed_os(self):  
    parts_ls = filter(lambda a: a.startswith('sd') and len(a)>3,os.listdir('/dev/'))
    lines = commands.getoutput('mount -v').split('\n')
    points_ls = map(lambda line: line.split()[2], lines)
    #fs_type_ls =  map(lambda line: line.split()[4], lines)
    mounted_ls = map(lambda line: line.split()[0], lines)
    mounted_dict = dict(zip(mounted_ls, points_ls))
    fs_root = mounted_ls[points_ls.index('/')]
    found_os_dic = {}
    for p in parts_ls:
      fp='/dev/%s' %p
      if fp in mounted_ls:
        if fp != fs_root:
          # search mounted partitions here
          mp=mounted_dict[fp]
          cur_os = self.guess_os(mp)
          if cur_os: found_os_dic[fp]=self.setup_item(int(cur_os), fp, mp)
      else:
        # search unmounted partitions here
        mp=os.path.join('/tmp/mnt',p)
        try: os.makedirs(mp)
        except OSError:pass
        c=commands.getstatusoutput('mount -t auto %s %s'%(fp,mp))
        cur_os = self.guess_os(mp)
        if cur_os: found_os_dic[fp]=self.setup_item(int(cur_os), fp, mp)
        c=commands.getstatusoutput('umount %s'%(mp))
    return found_os_dic

  def set_grub_items(self):
    cfg_fn='/boot/grub/grub.conf'
    self.rm_old_items(cfg_fn)
    found_os_dic=self.find_installed_os()
    items=map(lambda a: a[1], found_os_dic.values())
    grub_items='\n'.join(items)
    new_items='\n#Start OCC items\n%s\n#End OCC items'%grub_items
    grub_cfg='%s\n%s'%(self.read_cfg(cfg_fn),new_items)
    self.write_cfg(cfg_fn, grub_cfg)
    ret_items=''
    for a in found_os_dic:
      ret_items+='\n%-20s %s' % (a,found_os_dic[a][0])
    return ret_items
  

