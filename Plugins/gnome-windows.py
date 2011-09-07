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
    PluginsClass.__init__(self, ccw,_('windows'),'gnome',45)
    vbox=gtk.VBox(False,2)
    vb=gtk.VBox(False,2)
    #FIXME: Toggle comment state for next 7 lines to disable expander 
    expander=gtk.Expander(_("Adjust windows settings"))
    expander.add(vbox)
    self.add(expander)
    #self.add(vbox)
    #h=gtk.HBox(False,0)
    #h.pack_start(gtk.Label(_('Adjust desktop fonts')),False,False,0)
    #vbox.pack_start(h,False,False,6)
    vbox.pack_start(vb,False,False,6)
    
    self.gconfsettings(vb)
    
    #if not ccw.GSettings:
    #  self.gconfsettings(vb)
    #else:
    #  self.GioSettings(vb, ccw)
    #  vbox.pack_start(resetButton(vb),False,False,1)

  def GioSettings(self, vb, ccw):
    # TODO: add window theme ( GTK3-theme )
    pass
  
  def gconfsettings(self,vb):
    # FIXME: User titled menu items
    TActions_ls=['lower', 'menu', 'minmize', 'none', 'shade', 'toggle_maximize', 
                   'toggle_maximize_horizontally', 'toggle_maximize_vertically', 'toggle_shade']
    FMode_ls=['click', 'mouse', 'sloppy']
    BTLayout_ls=[':close', ':minimize', ':maximize', ':minimize,close',
                 ':maximize,close', ':minimize,maximize', ':minimize,maximize,close']
    # TODO: add the fallback (metacity) window theme
    L=( \
      (_('Action on title bar double-click'), '/apps/metacity/general/action_double_click_titlebar', TActions_ls, ''),
      (_('Action on title bar middle-click'), '/apps/metacity/general/action_middle_click_titlebar', TActions_ls, ''),
      (_('Action on title bar right-click'), '/apps/metacity/general/action_right_click_titlebar', TActions_ls, ''),
      (_('Window focus mode'), '/apps/metacity/general/focus_mode', FMode_ls, ''),
      (_('Windows button layout'), '/desktop/gnome/shell/windows/button_layout', BTLayout_ls, _('Require Gnome-Shell Restart'))
      )
    GC = gconf.client_get_default()
    for t,k,l,h in L:
      GC.add_dir(os.path.dirname(k),gconf.CLIENT_PRELOAD_NONE)
      cb=comboBox(t,k,GC, l)
      cb.set_tooltip_text(h)
      vb.pack_start(cb,False,False,1)

