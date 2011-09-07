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
import gconf
import os
from OjubaControlCenter.pluginsClass import PluginsClass
from OjubaControlCenter.gwidgets import resetButton, comboBox, hscale, fontButton

class occPlugin(PluginsClass):
  def __init__(self,ccw):
    PluginsClass.__init__(self, ccw,_('Desktop Fonts'),'gnome',30)
    vbox=gtk.VBox(False,2)
    vb=gtk.VBox(False,2)
    #FIXME: Toggle comment state for next 7 lines to disable expander 
    expander=gtk.Expander(_("Adjust desktop fonts"))
    expander.add(vbox)
    self.add(expander)
    #self.add(vbox)
    #h=gtk.HBox(False,0)
    #h.pack_start(gtk.Label(_('Adjust desktop fonts')),False,False,0)
    #vbox.pack_start(h,False,False,6)
    vbox.pack_start(vb,False,False,6)
    
    if not ccw.GSettings:
      self.gconfsettings(vb)
    else:
      self.GioSettings(vb, ccw)
      vbox.pack_start(resetButton(vb),False,False,1)

  def GioSettings(self, vb, ccw):
    P='org.gnome.desktop.interface'
    GS = ccw.GSettings(P)
    s=hscale(_('Text scaling factor'), 'text-scaling-factor',GS)
    vb.pack_start(s,False,False,6)
    FB_l=( \
       (_('Default font'),'font-name'),
       (_('Document font'),'document-font-name'),
       (_('Monospace font'),'monospace-font-name'),
    )
    for t,k in FB_l:
      b=fontButton(t,k,GS)
      vb.pack_start(b,False,False,1)
    self.gconfsettings(vb)
    P='org.gnome.settings-daemon.plugins.xsettings'
    GS = ccw.GSettings(P)
    FD_l=( \
       (_('Hinting'),'hinting'),
       (_('Antialiasing'),'antialiasing')
    )
    for t,k in FD_l:
      cb=comboBox(t,k,GS, GS.get_range(k)[1])
      vb.pack_start(cb,False,False,1)
  
  def gconfsettings(self,vb):
    GC = gconf.client_get_default()
    P = '/apps/metacity/general/titlebar_font'
    GC.add_dir(os.path.dirname(P),gconf.CLIENT_PRELOAD_NONE)
    vb.pack_start(fontButton(_('Window title'),P,GC),False,False,1)
