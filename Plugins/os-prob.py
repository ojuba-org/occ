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
from OjubaControlCenter.widgets import InstallOrInactive, sure, info, error, wait
from OjubaControlCenter.pluginsClass import PluginsClass

class occPlugin(PluginsClass):
  def __init__(self,ccw):
    PluginsClass.__init__(self, ccw,_('Installed systems:'),'boot',40)
    vb=Gtk.VBox(False,2)
    self.add(vb)

    h=Gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    l=Gtk.Label(_("This section will help you to search your disks \nfor installed system and add them to grub menu"))
    h.pack_start(l, False,False,2)
    
    
    h=Gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    m=InstallOrInactive(self, _("Install os prober"),_("os prober is installed"), _('package detects other OSes available on a system'), ['os-prober'])
    h.pack_start(m,False,False,2)
    self.apply_b = b = Gtk.Button(_('Find and add installed systems to grub menu'))
    b.set_sensitive(not m.get_sensitive())
    b.connect('clicked', self.apply_cb)
    h.pack_start(b, False,False,2)
    
  def apply_cb(self, w):
    if not sure(_('Are you sure you want to detect and add other operating systems?'), self.ccw): return
    dlg=wait(self.ccw)
    dlg.show_all()
    r=self.ccw.mechanism('grub2','os_prober_cb')
    dlg.hide()
    if r == 'NotAuth': return 
    if r.startswith("Error"): return info('%s: %s'%(_('Error'),r[6:]))
    info(_('Operating systems found:\n%s') % r,self.ccw)
    
