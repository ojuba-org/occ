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

class occPlugin(PluginsClass):
  def __init__(self,ccw):
    PluginsClass.__init__(self, ccw,_('windows'),'gnome',45)
    description=_("Adjust windows settings")
    self.GConf=ccw.GConf
    creatVBox(self, ccw, description, self.gconfsettings, self.gconfsettings, False) 

  def GioSettings(self, vb, ccw):
    pass
  
  def gconfsettings(self, vb, ccw):
    if not self.GConf: return False
    TActions_ls=['lower', 'menu', 'minmize', 'none', 'shade', 'toggle_maximize', 
                   'toggle_maximize_horizontally', 'toggle_maximize_vertically', 'toggle_shade']
    FMode_ls=['click', 'mouse', 'sloppy']
    BTLayout_ls=[':close', ':minimize', ':maximize', ':minimize,close',
                 ':maximize,close', ':minimize,maximize', ':minimize,maximize,close']
    L=( \
      (_('Action on title bar double-click'), '/apps/metacity/general/action_double_click_titlebar', TActions_ls, ''),
      (_('Action on title bar middle-click'), '/apps/metacity/general/action_middle_click_titlebar', TActions_ls, ''),
      (_('Action on title bar right-click'), '/apps/metacity/general/action_right_click_titlebar', TActions_ls, ''),
      (_('Window focus mode'), '/apps/metacity/general/focus_mode', FMode_ls, ''),
      (_('Windows button layout'), '/desktop/gnome/shell/windows/button_layout', BTLayout_ls, _('Require Gnome-Shell Restart'))
      )
    GC, CPT = self.GConf
    for t,k,l,h in L:
      GC.add_dir(os.path.dirname(k),CPT)
      cb=comboBox(t,k,GC, l)
      cb.set_tooltip_text(h)
      vb.pack_start(cb,False,False,1)

