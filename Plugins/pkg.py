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

from gi.repository import Gtk
import re
import os.path
from glob import glob
from OjubaControlCenter.widgets import LaunchButton, info, error, sure
from OjubaControlCenter.pluginsClass import PluginsClass
import dbus
#import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
dbus_loop = DBusGMainLoop(set_as_default = True)
bus = dbus.SystemBus()
interface = 'org.freedesktop.UDisks'


class occPlugin(PluginsClass):
  keep_cache_re=re.compile(r"^(\s*keepcache)\s*=\s*(.*)\s*$",re.M)
  media_repo_save='/etc/occ/media-repo.save'
  def __init__(self,ccw):
    self.__dev = bus.get_object(interface, "/org/freedesktop/UDisks")
    PluginsClass.__init__(self, ccw,_('Package Manager:'),'install', 10)
    vb=Gtk.VBox(False,2)
    self.add(vb)
    h=Gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    l=Gtk.Label(_('Package Manager allows you to install software.\nIt saves you the effort downloading, tracing versions and resolving dependencies.'))
    h.pack_start(l,False,False,2)
    h=Gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    h.pack_start(LaunchButton(_("Add/Remove applications"), fn='/usr/bin/gpk-application',icon="system-software-install"),False,False,2)
    h.pack_start(LaunchButton(_("KPackageKit"), fn='/usr/bin/kpackagekit'), False,False,2)
    h.pack_start(LaunchButton(_("Yum Extender"), fn='/usr/bin/yumex'), False,False,2)
    h=Gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    l=Gtk.Label(_('Package Manager uses predefined software sources (called repositories) to get software.\nBy using official repositories you will get signed packages.'))
    h.pack_start(l,False,False,2)
    h=Gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    h.pack_start(LaunchButton(_("Software Sources Editor"), fn='/usr/bin/gpk-repo'),False,False,2)
    h=Gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    l=Gtk.Label(_("You may add installation medium (CD/DVD) which contains packages.\nThey are used to install packages offline or save bandwidth.\nSome people consider inserting media annoying and prefer to download packages over the internet."))
    h.pack_start(l,False,False,2)
    h=Gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    b=Gtk.Button(_('Add a media repository'))
    b.connect('clicked', self.add_media)
    h.pack_start(b, False,False,2)
    b=Gtk.Button(_('Disable all media repositories'))
    b.connect('clicked', self.disable_mediarepo)
    h.pack_start(b, False,False,2)
    
    h=Gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    l=Gtk.Label(_("If you don't have internet access you may want to disable internet repositories."))
    h.pack_start(l,False,False,2)
    h=Gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    b=Gtk.Button(_('Disable all internet repositories'))
    b.connect('clicked', self.disable_net_repos)
    h.pack_start(b, False,False,2)
    self.restore_repos_b=b=Gtk.Button(_('Restore enabled repositories'))
    b.set_tooltip_text(_("Restore the enabled repositories as they were before disabling internet repositories"))
    b.connect('clicked', self.restore_repos)
    h.pack_start(b, False,False,2)
    self.restore_repos_b.set_sensitive(os.path.exists(self.media_repo_save))

    h=Gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    l=Gtk.Label(_('You may keep the downloaded packages to pass them to other people.\nThose packages are kept under /var/cache/yum'))
    h.pack_start(l,False,False,2)
    h=Gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    self.keep_cache_b=Gtk.CheckButton(_('keep downloaded packages'))
    self.keep_cache_b.set_active(self.get_keep_cache())
    try:
      self.ccw.rm_old_rpms_b.set_sensitive(self.keep_cache_b.get_active())
      self.ccw.cp_new_rpms_b.set_sensitive(self.keep_cache_b.get_active())
    except: pass
    h.pack_start(self.keep_cache_b, False,False,2)
    b=Gtk.Button(stock=Gtk.STOCK_APPLY)
    b.connect('clicked', self.keep_cache)
    h.pack_start(b, False,False,2)

  def get_device_property(self, udi, key):
    dev=bus.get_object(interface, udi)
    return dev.Get(interface+'.Device', key, dbus_interface="org.freedesktop.DBus.Properties")

  def add_media(self, b):
    if not sure(_('Please make sure the media you want to add is inserted before you add it.\nDo you want to continue?'), self.ccw): return
    repos=[]
    l=self.__dev.EnumerateDevices(dbus_interface = interface)
    for udi in l:
      if self.get_device_property(udi, "device-is-removable"):
        if not bool(self.get_device_property(udi, 'device-is-mounted')):
          dev=bus.get_object(interface, udi)
          try:
            r = str(dev.FilesystemMount('auto', dbus.Array(dbus.String()), dbus_interface = interface+".Device")) or None
          except dbus.exceptions.DBusException:
            continue
        mnt=self.get_device_property(udi, 'device-mount-paths')
        if not mnt: continue
        mnt=str(mnt[0])
        repo=os.path.join(mnt,'media.repo')
        if os.path.exists(repo): repos.append(repo)
    if len(repos)==0: error(_("No valid media were found."), self.ccw); return
    r=self.ccw.mechanism('pkg','add_media',*repos)
    if r == 'NotAuth': return
    info(_('Done. %s repositories were added.\nOpen the package manager to load or refresh cache.') % r, self.ccw)

  def disable_mediarepo(self, b):
    r=self.ccw.mechanism('pkg','disable_mediarepo')
    if r == 'NotAuth': return
    info(_('Done. %s repositories were disabled.') % r, self.ccw)

  def get_keep_cache(self):
    c=open('/etc/yum.conf','rt').read()
    l=self.keep_cache_re.findall(c)
    if not l: return False
    v=l[-1][1].strip().lower()
    if v=='1' or v=='yes' or v=='true': return True
    return False

  def keep_cache(self, b):
    v=('0','1')[self.keep_cache_b.get_active()]
    r=self.ccw.mechanism('pkg','set_keep_cache', v)
    if r == 'NotAuth': return
    self.keep_cache_b.set_active(self.get_keep_cache())
    try:
      self.ccw.rm_old_rpms_b.set_sensitive(self.keep_cache_b.get_active())
      self.ccw.cp_new_rpms_b.set_sensitive(self.keep_cache_b.get_active())
    except: pass
    info(_('Done.'), self.ccw)

  def disable_net_repos(self, b):
    r=self.ccw.mechanism('pkg','disable_net_repos')
    if r == 'NotAuth': return
    self.restore_repos_b.set_sensitive(os.path.exists(self.media_repo_save))
    try: i=int(r)
    except ValueError: i==0
    if i<=0:
      info(_('no repository was disabled'), self.ccw)
    info(_('Done. %d repositories were disabled') % i, self.ccw)

  def restore_repos(self, b):
    r=self.ccw.mechanism('pkg','restore_enabled_repos')
    if r == 'NotAuth': return
    self.restore_repos_b.set_sensitive(os.path.exists(self.media_repo_save))
    try: i=int(r)
    except ValueError: i==0
    if i<=0:
      info(_('no repository was enabled'), self.ccw)
    info(_('Done. %d repositories were enabled') % i, self.ccw)

