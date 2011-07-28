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
from OjubaControlCenter.pluginsClass import PluginsClass
from OjubaControlCenter.gwidgets import resetButton, GSCheckButton, comboBox

class occPlugin(PluginsClass):
  def __init__(self,ccw):
    PluginsClass.__init__(self, ccw,_('Shell'),'gnome',40)
    vbox=gtk.VBox(False,2)
    vb=gtk.VBox(False,2)
    self.add(vbox)
    h=gtk.HBox(False,0)
    h.pack_start(gtk.Label(_('Shell interface setup')),False,False,0)
    vbox.pack_start(h,False,False,6)
    vbox.pack_start(vb,False,False,6)

    if not ccw.GSettings:
      h=gtk.HBox(False,0)
      h.pack_start(gtk.Label(_('Not installed')),False,False,0)
      vbox.pack_start(h,False,False,6)
    else:
      self.GioSettings(vb, ccw)
      vbox.pack_start(resetButton(vb),False,False,1)
    
  def GioSettings(self, vb, ccw):
    P='org.gnome.desktop.interface'
    GS = ccw.GSettings(P)
    tf=comboBox(_('Clock format'),'clock-format',GS, GS.get_range('clock-format')[1])
    vb.pack_start(tf,False,False,1)
    P='org.gnome.shell.clock'
    GS = ccw.GSettings(P)
    DT_l=( \
       (_('Show seconds in clock'),'show-seconds'),
       (_('Show date in clock'),'show-date')
    )
    
    for t,k in DT_l:
      g=GSCheckButton(t,k,GS)
      vb.pack_start(g,False,False,1)


