# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent syntax=python
# -*- Mode: Python; py-indent-offset: 4 -*-
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
from OjubaControlCenter.pluginsClass import PluginsClass
from OjubaControlCenter.gwidgets import resetButton, comboBox, creatVBox

## NOTE: these global vars is loader validators
category = 'gnome'
caption = _('Power settings')
description = _("Adjust power settings")
priority = 60

class occPlugin(PluginsClass):
    def __init__(self,ccw):
        PluginsClass.__init__(self, ccw, caption, category, priority)
        creatVBox(self, ccw, description, self.GioSettings) 
        
    def GioSettings(self, vb, ccw):
        P='org.gnome.settings-daemon.plugins.power'
        if not P in ccw.GSchemas_List: return False
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
        return True
