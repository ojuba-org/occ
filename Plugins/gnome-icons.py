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
import os
import os.path
import gconf
import gtk

from OjubaControlCenter.pluginsClass import PluginsClass

class gconfCheckButton(gtk.CheckButton):
  def __init__(self,caption,p,c):
    gtk.CheckButton.__init__(self,caption)
    self.c=c
    self.p=p
    self.update()
    self.c.add_dir(os.path.dirname(self.p),gconf.CLIENT_PRELOAD_NONE)
    self.c.notify_add(self.p, self.update)
    self.connect('toggled',self.__set_gconf)
  def __set_gconf(self,*args):
    self.c.set_bool(self.p, self.get_active())

  def update(self,*args, **kw):
    v=self.c.get_bool(self.p)
    if v!=self.get_active(): self.set_active(v)


class occPlugin(PluginsClass):
  def __init__(self,ccw):
    PluginsClass.__init__(self, ccw,_('Desktop Icons'),'gnome')
    vb=gtk.VBox(False,2)
    self.add(vb)
    self.c=gconf.client_get_default()
    h=gtk.HBox(False,0)
    h.pack_start(gtk.Label(_('Select the icons you want to be visible on desktop')),False,False,0)
    vb.pack_start(h,False,False,6)
    P='/apps/nautilus/desktop/'
    l=( \
       (_('Computer'),P+'computer_icon_visible'),
       (_('Home'),P+'home_icon_visible'),
       (_('Network'),P+'network_icon_visible'),
       (_('Trash'),P+'trash_icon_visible'),
       (_('Mounted volumes'),P+'volumes_visible')
    )
    for t,p in l:
      g=gconfCheckButton(t,p,self.c)
      vb.pack_start(g,False,False,1)

