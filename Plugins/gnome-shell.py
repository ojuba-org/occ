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

import os, os.path
import gtk 
from OjubaControlCenter.pluginsClass import PluginsClass
from OjubaControlCenter.gwidgets import resetButton, GSCheckButton, comboBox, creatVBox
from OjubaControlCenter.widgets import LaunchFileManager

class occPlugin(PluginsClass):
  def __init__(self,ccw):
    PluginsClass.__init__(self, ccw,_('Shell'),'gnome',40)
    description=_("Shell interface setup")
    creatVBox(self, ccw, description, self.GioSettings) 

  def GioSettings(self, vb, ccw):
    P='org.gnome.desktop.interface'
    if not P in ccw.GSchemas_List: return False
    h=gtk.HBox(False,0)
    h.pack_start(LaunchFileManager(_("Personal shell extensions folder"), os.path.expanduser('~/.local/share/gnome-shell/')),False,False,2)
    vb.pack_start(h,False,False,6)
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
    return True

