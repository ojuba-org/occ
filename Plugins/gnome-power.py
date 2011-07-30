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
import os.path
import logging
import gtk 
from OjubaControlCenter.pluginsClass import PluginsClass
from OjubaControlCenter.gwidgets import resetButton, comboBox

class occPlugin(PluginsClass):
  def __init__(self,ccw):
    PluginsClass.__init__(self, ccw,_('Power settings'),'gnome',60)
    vbox=gtk.VBox(False,2)
    vb=gtk.VBox(False,2)
    self.add(vbox)
    h=gtk.HBox(False,0)
    h.pack_start(gtk.Label(_('Adjust power settings')),False,False,0)
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
    P='org.gnome.settings-daemon.plugins.power'
    GS = ccw.GSettings(P)
    FD_l=( \
       (_('Power button'),'button-power'),
       (_('Hibernate button'),'button-hibernate'),
       (_('Sleep button'),'button-sleep'),
       (_('Suspend button'),'button-suspend'),
       #(_('Cursor theme'),'button-sleep'),
       (_('Critical battery action'),'critical-battery-action'),
       (_('Laptop lid close action on AC'),'lid-close-ac-action'),
       (_('Laptop lid close action on battery'),'lid-close-battery-action'),
       (_('Sleep inactive type on AC'),'sleep-inactive-ac-type'),
       (_('Sleep inactive type on power'),'sleep-inactive-battery-type')
    )
    for t,k in FD_l:
      cb=comboBox(t,k,GS, GS.get_range(k)[1])
      vb.pack_start(cb,False,False,1)

