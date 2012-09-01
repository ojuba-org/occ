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
from OjubaControlCenter.utils import *
from OjubaControlCenter.pluginsClass import PluginsClass
from OjubaControlCenter.widgets import LaunchFileButton, sure, info, error

## NOTE: these global vars is loader validators
category = 'boot'
caption = _('Boot options')
description = ''
priority = 50

class occPlugin(PluginsClass):
  __resolutions={
  '640x480x8':0x301,	'640x480x15':0x310,	'640x480x16':0x311,	'640x480x24':0x312,
  '800x600x8':0x303,	'800x600x15':0x313,	'800x600x16':0x314,	'800x600x24':0x315,
  '1024x768x8':0x305,	'1024x768x15':0x316,	'1024x768x16':0x317,	'1024x768x24':0x318,
  '1280x1024x8':0x307,	'1280x1024x15':0x319,	'1280x1024x16':0x31A,	'1280x1024x24':0x31B,
}
  resolutions_ls=[_('Default')]
  resolutions_ls.extend(sorted(__resolutions.keys()))
  def __init__(self,ccw):
    PluginsClass.__init__(self, ccw, caption, category, priority)
    vb=Gtk.VBox(False,2)
    self.add(vb)
    hb=Gtk.HBox(False,0)
    vb.pack_start(hb,False,False,0)
    hb.pack_start(Gtk.Label(_('Graphical Boot:')),False,False,0)
    self.__vga_ls=Gtk.ComboBoxText()
    #self.__vga_ls.append_text(_('Default'))
    for i in self.resolutions_ls:
      self.__vga_ls.append_text(i)
    self.__vga_ls.set_active(0)
    hb.pack_start(self.__vga_ls,False,False,0)
    b=Gtk.Button(stock=Gtk.STOCK_APPLY)
    b.connect('clicked', self.__apply_cb)
    hb.pack_start(b,False,False,0)

  def __apply_cb(self, b):
    active = self.resolutions_ls[self.__vga_ls.get_active()]
    n=self.__resolutions.get(active,None)
    if not n: self.ccw.mechanism('vga', 'rm_kernel_vga')
    else: self.ccw.mechanism('vga', 'set_kernel_vga', str(n))
    info(_('Done!'), self.ccw)
