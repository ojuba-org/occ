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
import os.path
from OjubaControlCenter.pluginsClass import PluginsClass
from OjubaControlCenter.gwidgets import resetButton, comboBox, hscale, fontButton, creatVBox

## NOTE: these global vars is loader validators
category = 'gnome'
caption = _('Desktop Fonts')
description = _("Adjust desktop fonts")
priority = 30

class occPlugin(PluginsClass):
  def __init__(self,ccw):
    PluginsClass.__init__(self, ccw, caption, category, priority)
    self.GConf=ccw.GConf
    creatVBox(self, ccw, description, self.GioSettings, self.gconfsettings) 

  def GioSettings(self, vb, ccw):
    P='org.gnome.desktop.interface'
    if not P in ccw.GSchemas_List: return False
    GS = ccw.GSettings(P)
    s=hscale(_('Text scaling factor'), 'text-scaling-factor',GS)
    vb.pack_start(s,False,False,6)
    FB_l=( \
       (_('Default font'),'font-name'),
       (_('Document font'),'document-font-name'),
       (_('Monospace font'),'monospace-font-name'),
    )
    for t,k in FB_l:
      b=fontButton(t,k,GS, ccw)
      vb.pack_start(b,False,False,1)
    self.gconfsettings(vb, ccw)
    P='org.gnome.settings-daemon.plugins.xsettings'
    if not P in ccw.GSchemas_List: return True
    GS = ccw.GSettings(P)
    FD_l=( \
       (_('Hinting'),'hinting'),
       (_('Antialiasing'),'antialiasing')
    )
    for t,k in FD_l:
      cb=comboBox(t,k,GS, GS.get_range(k)[1])
      vb.pack_start(cb,False,False,1)
    return True
    
  def gconfsettings(self, vb, ccw):
    if not self.GConf: return False
    GC,CPT = self.GConf
    P = '/apps/metacity/general/titlebar_font'
    GC.add_dir(os.path.dirname(P),CPT)
    vb.pack_start(fontButton(_('Window title'),P,GC, ccw),False,False,1)
