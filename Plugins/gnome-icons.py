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
from OjubaControlCenter.pluginsClass import PluginsClass
from OjubaControlCenter.gwidgets import resetButton, GSCheckButton, mainGSCheckButton

class occPlugin(PluginsClass):
  def __init__(self,ccw):
    PluginsClass.__init__(self, ccw,_('Desktop Icons'),'gnome',20)
    vbox=gtk.VBox(False,2)
    vb=gtk.VBox(False,2)
    #FIXME: Toggle comment state for next 7 lines to disable expander
    expander=gtk.Expander(_("Select the icons you want to be visible on desktop"))
    expander.add(vbox)
    self.add(expander)
    #self.add(vbox)
    #h=gtk.HBox(False,0)
    #h.pack_start(gtk.Label(_('Select the icons you want to be visible on desktop')),False,False,0)
    #vbox.pack_start(h,False,False,6)
    vbox.pack_start(vb,False,False,1)
    
    if not ccw.GSettings:
      h=gtk.HBox(False,0)
      h.pack_start(gtk.Label(_('Not installed')),False,False,0)
      vbox.pack_start(h,False,False,6)
    else:
      self.GioSettings(vb, ccw)
      vbox.pack_start(resetButton(vb),False,False,1)
    
  def GioSettings(self, vb, ccw):
    SD_P='org.gnome.desktop.background'
    DT_P='org.gnome.nautilus.desktop'
    
    GS = ccw.GSettings(SD_P)
    c=mainGSCheckButton(vb,_('Show desktop icons'),'show-desktop-icons',GS)
    vb.pack_start(c,False,False,1)
    GS = ccw.GSettings(DT_P)
    DT_l=( \
       (_('Computer'),'computer-icon-visible'),
       (_('Home'),'home-icon-visible'),
       (_('Network'),'network-icon-visible'),
       (_('Trash'),'trash-icon-visible'),
       (_('Mounted volumes'),'volumes-visible')
    )
    for t,k in DT_l:
      g=GSCheckButton(t,k,GS)
      vb.pack_start(g,False,False,1)
    c.update_cboxs()
    

