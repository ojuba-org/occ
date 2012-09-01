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
from OjubaControlCenter.utils import chkconfig
from OjubaControlCenter.pluginsClass import PluginsClass
from OjubaControlCenter.widgets import InstallOrInactive, error, info, sure

## NOTE: these global vars is loader validators
category = 'net'
caption = _('Dialup modem')
description = _("Some software dialup modems are supported by slmodem driver.\nIf you have a supported modem select a proper interface for it and activate its daemon before using it.")
priority = 100

class occPlugin(PluginsClass):
  def __init__(self,ccw):
    PluginsClass.__init__(self, ccw, caption, category, priority)
    vb=Gtk.VBox(False,2)
    self.add(vb)
    hb=Gtk.HBox(False,6); vb.pack_start(hb,True,True,2)
    hb.pack_start(Gtk.Label(description),False,False,2)
    hb=Gtk.HBox(False,6); vb.pack_start(hb,True,True,2)
    hb.pack_start(InstallOrInactive(self, _("Install slmodem driver"),_("slmodem driver is installed"), _('driver for some software modems'), ['kmod-slmodem']),False,False,2)
    self.sl_service=Gtk.CheckButton(_("Start slmodem daemon on boot"))
    self.__sl_service_internal=False
    self.sl_service.set_active(chkconfig(5,'slmodem'))
    self.sl_service.connect('toggled', self.sl_service_cb)
    hb.pack_start(self.sl_service,False,False,2)
    hb=Gtk.HBox(False,6); vb.pack_start(hb,True,True,2)
    self.interface_ls=Gtk.ComboBoxText()
    self.interface_ls.append_text("alsa")
    self.interface_ls.append_text("slamr")
    self.interface_ls.append_text("slusb")
    self.interface_ls.set_active(0)
    hb.pack_start(self.interface_ls,False,False,2)
    b=Gtk.Button(stock=Gtk.STOCK_APPLY)
    b.connect('clicked',self.interface_cb)
    hb.pack_start(b,False,False,2)

  def sl_service_cb(self, b):
    if self.__sl_service_internal: return
    cmd="chkconfig --level 2345 slmodem %s" % ('off','on')[self.sl_service.get_active()]
    r=self.ccw.mechanism('run','system', cmd)
    if r == 'NotAuth': return
    self.__sl_service_internal=True
    self.sl_service.set_active(chkconfig(5,'slmodem'))
    self.__sl_service_internal=False
    if r!='0':
      error(_('unexpected return code, possible an error had occurred.'), self.ccw)

  def interface_cb(self, b):
    i=self.interface_ls.get_active_text()
    r=self.ccw.mechanism('modem','set_sl_interface', i)
    if r == 'NotAuth': return
    if r!='0': error(_('unexpected return code, possible an error had occurred.'), self.ccw)

