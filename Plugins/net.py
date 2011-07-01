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
import re
import gtk

from glob import glob
from OjubaControlCenter.utils import chkconfig
from OjubaControlCenter.widgets import LaunchOrInstall, sure, info, error
from OjubaControlCenter.pluginsClass import PluginsClass

class occPlugin(PluginsClass):
  comments_re=re.compile('#.*$',re.M)
  def __init__(self,ccw):
    PluginsClass.__init__(self, ccw, _('Network settings:'),'net',10)
    vb=gtk.VBox(False,2)
    self.add(vb)   
    hb=gtk.HBox(False,2); vb.pack_start(hb,False,False,6)
    l=gtk.Label(_("""Network Manager applet is the little icon you see on your system tray.
You can use it to edit your connections."""))
    hb.pack_start(l, False,False,2)

    hb=gtk.HBox(False,2)
    vb.pack_start(hb,False,False,2)
    hb.pack_start(LaunchOrInstall(self, _('Connection Editor'), '/usr/bin/nm-connection-editor',pkgs=['NetworkManager-gnome']),False,False,0)


    hb=gtk.HBox(False,2)
    vb.pack_start(hb,False,False,2)
    l=gtk.Label(_("""The legacy Network Configuration tool can give you more detailed privileged control over your network.\nIf you have used it please click "Suggest" button"""))
    hb.pack_start(l, False,False,2)
    hb=gtk.HBox(False,2)
    vb.pack_start(hb,False,False,2)
    hb.pack_start(LaunchOrInstall(self, _('Network Configuration'), '/usr/bin/system-control-network',pkgs=['system-config-network']),False,False,0)
    b=gtk.Button(_('Suggest'))
    b.connect('clicked',self.suggest_cb)
    hb.pack_start(b,False,False,0)

  def nic_parse(self, nic):
      try: t=open(nic,'rt').read()
      except IOError: return None
      t=self.comments_re.sub('',t).splitlines()
      t=filter(lambda j: not j.startswith('#'), map(lambda i: i.strip(), t))
      m=filter(lambda j: len(j)==2, map(lambda i: i.split('=',1),open(nic,'rt').read().splitlines()))
      m=map(lambda i: (i[0].strip(),i[1].strip()),m) # not needed but just to be sure
      d=dict(m)
      return d

  def suggest_cb(self, b):
    nic_list=glob('/etc/sysconfig/networking/devices/*')
    nm=0
    for nic in nic_list:
      d=self.nic_parse(nic)
      if not d: continue
      ch=0
      if d.get('ONBOOT','yes')!='yes' and sure(_("The device [%s] named [%s] is not set to be started automatically on each boot.\nDo you like to start it automatically on boot?") % (d['DEVICE'], d.get('NAME','unnamed'))):
        self.ccw.mechanism('net','nic_set_onboot', nic)

      if d.get('NM_CONTROLLED','yes')!='yes' and sure(_("The device [%s] named [%s] is not set to be controlled with Network Manager.\nDo you like to allow Network Manager to control this device?") % (d['DEVICE'], d.get('NAME','unnamed'))):
        self.ccw.mechanism('net','nic_set_nm', nic)
        ch=1

      if d.get('USERCTL','yes')!='yes' and sure(_("The device [%s] named [%s] is not allowed to be controlled by unprivileged users.\nDo you like to allow them?") % (d['DEVICE'], d.get('NAME','unnamed'))):
        self.ccw.mechanism('net','nic_set_userctl', nic)
      # if something is changed reload conf
      if ch: d=self.nic_parse(nic)
      if not d: continue
      if d.get('NM_CONTROLLED','yes')!='yes': nm|=1

    fix_nm_service=chkconfig(5, 'network') or not chkconfig(5, 'NetworkManager')
    if nm and fix_nm_service and sure(_("Network Manager is used by some device, but you are using the legacy network service.\nWould you like to fix that?") % (d['DEVICE'], d.get('NAME','unnamed'))):
      self.ccw.mechanism('net','set_nm_service', nic)
    info(_("We got no more suggestions.\nIf you have made any changes it will take effect on next boot"))


# /etc/samba/smb.conf
#	usershare path = /var/lib/samba/usershare
#	usershare max shares = 100
#	usershare allow guests = yes
#	usershare owner only = no

