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
import gtk
import pango
import os, os.path
import re
import shutil
from glob import glob
from OjubaControlCenter.widgets import LaunchFileManager,NiceButton,sure,info
from OjubaControlCenter.pluginsClass import PluginsClass
class occPlugin(PluginsClass):
  __ch_re=re.compile(r'\\(0\d\d)')
  def __init__(self,ccw):
    PluginsClass.__init__(self, ccw,_('Installing fonts:'),'desktop')
    vb=gtk.VBox(False,2)
    self.add(vb)
    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    l=gtk.Label(_('Open your personal fonts folder and manage your fonts there.\nJust drag and drop or copy and past font files there.'))
    h.pack_start(l,False,False,2)
    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    p=os.path.expanduser('~/.fonts/')
    if not os.path.exists(p): os.mkdir(p)
    h.pack_start(LaunchFileManager(_("Personal fonts folder"), os.path.expanduser('~/.fonts/'),stock=gtk.STOCK_SELECT_FONT),False,False,2)

    #b=gtk.Button(_("System fonts folder"))
    #b.connect('clicked',self.__sys_fonts_cb)
    #h.pack_start(b,False,False,2)
    
    b=NiceButton(_("Import fonts from another installed OS"),stock=gtk.STOCK_CONVERT)
    b.connect('clicked',self.import_fonts)
    h.pack_start(b,False,False,2)
  def __sys_fonts_cb(self,b):
    self.ccw.mechanism('run','fileman','/usr/share/fonts/')

  def import_fonts(self,*args):
    M=("ar", "co", "ta","ti","tr", "ve")
    f=[]
    m=[]
    d=[]
    if not sure(_("Are you sure you want to search and install fonts ?\nMake sure that the partitions are mounted and you have a license to use the fonts.\n")): return
    for i in open('/proc/mounts','rt'):
      p=self.__ch_re.sub(lambda m: chr(int(m.group(1),8)), i.split()[1].strip())
      if p=='/': continue
      d.extend(glob(os.path.join(p,'*','[Ff][Oo][Nn][Tt][Ss]')))
    for i in d:
      f.extend(glob(os.path.join(i,'*.[Tt][Tt][Ff]')))
    # make f uniq
    k={}
    for i in f: k[os.path.basename(i).lower()]=i
    f=k.values()
    
    m=filter(lambda i: os.path.basename(i).lower()[:2] in M,f)
    a=True
    lf,lm=len(f),len(m)
    if lf-lm>10: a=sure(_("There are %i fonts found, only %i could be important to you. Do you want to install all the fonts?\n") % (lf,lm))
    d=os.path.expanduser('~/.fonts/')
    if not os.path.exists(d): os.mkdir(d)
    os.system('xdg-open "%s"' % d)
    if not a: f=m
    for i in f:
      shutil.copy(i,d)
    info(_("Done. %d font were installed.") % len(f))

