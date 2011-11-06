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
import gtk
from subprocess import *
from OjubaControlCenter.widgets import LaunchOrInstall, sure, info, error
from OjubaControlCenter.utils import chkconfig
from OjubaControlCenter.pluginsClass import PluginsClass

class occPlugin(PluginsClass):
  ushare_path_re=re.compile(r'''^(\s*\[global\][^\[]*)^\s*(usershare\s+path[ \t]*=[ \t]*([^\n]*))\s*$''',re.M | re.S)
  def __init__(self,ccw):
    PluginsClass.__init__(self, ccw, _('Advanced Network settings:'),'net',20)
    vb=gtk.VBox(False,2)
    self.add(vb)   
    hb=gtk.HBox(False,2); vb.pack_start(hb,False,False,6)
    l=gtk.Label(_("""Firewall protects your system by filtering unwanted network access."""))
    hb.pack_start(l, False,False,2)

    hb=gtk.HBox(False,2)
    vb.pack_start(hb,False,False,2)
    hb.pack_start(LaunchOrInstall(self, _('Configure firewall'), '/usr/bin/system-config-firewall',pkgs=['system-config-filewall']),False,False,0)

    hb=gtk.HBox(False,2)
    vb.pack_start(hb,False,False,2)
    l=gtk.Label(_("""Samba is used to share folders and printers in LAN"""))
    hb.pack_start(l, False,False,2)
    hb=gtk.HBox(False,2); vb.pack_start(hb,False,False,2)
    if not self.is_smb_on():
      b=gtk.Button(_("Start samba on boot"))
      b.connect('clicked', self.smb_service_on)
      hb.pack_start(b,False,False,0)
    hb.pack_start(LaunchOrInstall(self, _('Create or modify shares'), '/usr/bin/system-config-samba',pkgs=['system-config-samba']),False,False,0)
    hb=gtk.HBox(False,2)
    vb.pack_start(hb,False,False,2)
    self.ushare=gtk.CheckButton(_('Allow unprivileged users to create shares'))
    self.ushare.set_active(self.is_ushare())
    hb.pack_start(self.ushare,False,False,0)
    b=gtk.Button(stock=gtk.STOCK_APPLY)
    b.connect('clicked', self.ushare_cb)
    hb.pack_start(b,False,False,0)

  def is_ushare(self):
    try: t=open('/etc/samba/smb.conf','rt').read()
    except IOError: return False
    if self.ushare_path_re.search(t): return True
    return False

  def is_smb_on(self):
    r=Popen(["runlevel"], stdout=PIPE).communicate()[0].split()
    if len(r)<2: r=5
    else:
      try: r=int(r[1])
      except ValueError: r=5
    chkconfig(r,'smb')

  def smb_service_on(self, b):
    r=self.ccw.mechanism('smb','start_on_boot')
    if r == 'NotAuth': return
    info(_('Done.'))

  def ushare_cb(self,b):
    r=self.ccw.mechanism('smb','enable_ushare', str(int(self.ushare.get_active())) )
    if r == 'NotAuth': return
    info(_('Done.'))

# 
# runlevel
