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
import json
import gtk 
from OjubaControlCenter.pluginsClass import PluginsClass
from OjubaControlCenter.widgets import LaunchFileManager
from OjubaControlCenter.gwidgets import creatVBox
class extHBox(gtk.HBox):
  def __init__(self, parent, ext):
    gtk.HBox.__init__(self,False,0)
    self.Parent=parent
    self.Uuid=self.Name=self.Description=self.Shell_version=''
    self.Url=self.Localedir=self.Path=''
    if ext.has_key('uuid'): self.Uuid=ext['uuid']
    if ext.has_key('name'): self.Name=ext['name']
    if ext.has_key('localedir'): self.Localedir=ext['localedir']
    if ext.has_key('description'): self.Description=ext['description']
    if ext.has_key('shell-version'): self.Shell_version=ext['shell-version']
    if ext.has_key('url'): self.Url=ext['url']
    if ext.has_key('path'): self.Path=ext['path']
    self.set_tooltip_text(self.Description)
    self.chkb = c = gtk.CheckButton(self.Name)
    c.set_active(self.Parent.is_enabled(self.Uuid))
    # TODO: check shell version compatibility
    c.set_sensitive(bool(self.Shell_version))
    c.connect('toggled',self.set_stat)
    self.pack_start(self.chkb,True,True,1)
  
  def set_stat(self, b):
    f=self.Parent.set_disabled
    if self.chkb.get_active(): f=self.Parent.set_enabled
    f(self.Uuid)
    
class occPlugin(PluginsClass):
  def __init__(self,ccw):
    PluginsClass.__init__(self, ccw,_('Gnome shell extension'),'gnome',50)
    self.key='enabled-extensions'
    self.dirs=['/usr/share/gnome-shell/extensions/','/home/ehab/.local/share/gnome-shell/extensions']
    self.extensions={}
    self.GS=None
    description=_("Gnome shell extension manager")
    creatVBox(self, ccw, description, self.GioSettings, resetBtton=False) 

  def GioSettings(self, vb, ccw):
    P='org.gnome.shell'
    if not P in ccw.GSchemas_List: print 'p';return False
    self.GS=ccw.GSettings(P)
    if not self.key in self.GS.keys(): print 'k';return False
    self.extensions=self.get_installed_dict()
    h=gtk.HBox(False,0)
    h.pack_start(LaunchFileManager(_("Personal shell extensions folder"), os.path.expanduser('~/.local/share/gnome-shell/')),False,False,2)
    vb.pack_start(h,False,False,6)
    
    for ext in self.extensions:
      c = extHBox(self, self.extensions[ext])
      vb.pack_start(c,False,False,6)
      
  def enabled_list(self):
    return self.GS.get_strv(self.key)
    
  def is_enabled(self, ext):
    e = self.enabled_list()
    return ext in e

  def set_disabled(self, ext):
    e = self.enabled_list()
    if ext in e: e.remove(ext)
    self.set_value(e)
    
  def set_enabled(self, ext):
    e = self.enabled_list()
    if not ext in e: e.append(ext)
    self.set_value(e)
  
  def set_value(self, l):
    self.GS.set_strv(self.key, l)
    
  def get_installed_dict(self):
    valid = self.walk_directories(self.dirs, lambda d:
             os.path.isdir(d)  and \
             os.path.exists(os.path.join(d, "metadata.json")) and \
             os.path.exists(os.path.join(d, "extension.js")))
    return valid
  def get_info(self, fn):
    return (open(fn, 'r').read().strip())
    
  def walk_directories(self, dirs, filter_func):
    valid = {}
    try:
      for thdir in dirs:
        if os.path.isdir(thdir):
          for t in os.listdir(thdir):
            p = os.path.join(thdir, t)
            if filter_func(os.path.join(thdir, t)):
              fn = os.path.join(p, "metadata.json")
              info = {u'name': t,'path': fn, u'uuid': t}
              try: info = json.loads(self.get_info(fn))
              except ValueError: pass
              try:
                if 'name' in info.keys():
                  info['path'] = p
              except AttributeError: pass
              valid[info['name']] = info
    except: pass
    return valid
  
