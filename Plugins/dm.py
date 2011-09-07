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
import gtk
import pwd
import os
import os.path
import re

from OjubaControlCenter.pluginsClass import PluginsClass
from OjubaControlCenter.widgets import info, error

class occPlugin(PluginsClass):
  dm_re=re.compile(r'''^\s*DISPLAYMANAGER\s*=\s*['"]?([^'"]+)['"]?\s*$''',re.M)
  def __init__(self,ccw):
    PluginsClass.__init__(self, ccw,_('Graphical Login Manager'),'desktop',150)
    vb=gtk.VBox(False,2)
    self.add(vb)
    hb=gtk.HBox(False,2); vb.pack_start(hb,True,True,6)
    l=gtk.Label(_("Display Manager is the application that allow you to log into your desktop.\nIt's the application that might ask you to authenticate with your username and password"))
    #l.set_line_wrap(True)
    hb.pack_start(l,False,False,2)
    hb=gtk.HBox(False,2); vb.pack_start(hb,True,True,2)
    self.dm_ls=['gdm','kdm','wdm','xdm']
    self.dm_ls=filter(lambda i: os.path.exists('/usr/sbin/'+i) or os.path.exists('/usr/bin/'+i),self.dm_ls)
    self.dm=gtk.combo_box_new_text()
    for i in self.dm_ls: self.dm.append_text(i)
    self.dm.set_active(self.get_current())
    hb.pack_start(gtk.Label(_("Available display managers:")),False,False,2)
    hb.pack_start(self.dm,False,False,2)
    b=gtk.Button(_("save change"))
    b.connect('clicked',self.set_dm)
    hb.pack_start(b,False,False,2)
    hb=gtk.HBox(False,2); vb.pack_start(hb,True,True,2)
    b=gtk.Button(_('Enable Automatic Login as this user'))
    b.connect('clicked',self.autologin_cb)
    hb.pack_start(b,False,False,2)
    b=gtk.Button(_('Disable Automatic Login'))
    b.connect('clicked',self.no_autologin_cb)
    hb.pack_start(b,False,False,2)

  def get_current(self):
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
      else: return 0
    v=v.lower()
    if v=='gnome': v='gdm'
    elif v=='kde': v='kdm'
    try: return self.dm_ls.index(v)
    except ValueError: return 0

  def set_dm(self,*args):
    i=self.dm.get_active_text()
    s=self.ccw.mechanism('run','system', 'system-switch-displaymanager "%s"' % i)
    if s=='0': info(_('Display manager is now set to %s') % i)
    else: error(_('Unable to set display managed.'))

  def autologin_cb(self, *args):
    u=pwd.getpwuid(os.geteuid())[0]
    s=self.ccw.mechanism('dm','enable_autologin', u)
    if s.startswith('-'): error(_('could not set automatic login in %s') % s[1:])
    elif s: info(_('Automatic login as %s was set in %s') % (u,s))
    else: error(_('could not set automatic login'))


  def no_autologin_cb(self, *args):
    s=self.ccw.mechanism('dm','disable_autologin')
    if not s: error(_('could not disable automatic login'))
    elif s.startswith('-'): error(_('could not disable automatic login in %s') % s[1:])
    else: info(_('automatic login is now disabled'))
    



