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
from OjubaControlCenter.gwidgets import resetButton, GSCheckButton, mainGSCheckButton, creatVBox

## NOTE: these global vars is loader validators
category = 'gnome'
caption = _('Desktop Icons')
description = _("Select the icons you want to be visible on desktop")
priority = 20

class occPlugin(PluginsClass):
    def __init__(self,ccw):
        PluginsClass.__init__(self, ccw, caption, category, priority)
        creatVBox(self, ccw, description, self.GioSettings) 
        
    def GioSettings(self, vb, ccw):
        P='org.gnome.desktop.background'
        if not P in ccw.GSchemas_List: return False
        GS = ccw.GSettings(P)
        if 'show-desktop-icons' in GS.list_keys():
            c=mainGSCheckButton(vb,_('Show desktop icons'),'show-desktop-icons',GS)
            vb.pack_start(c,False,False,1)
        P='org.gnome.nautilus.desktop'
        if not P in ccw.GSchemas_List: return True
        GS = ccw.GSettings(P)
        DT_l=( \
             (_('Home'),'home-icon-visible'),
             (_('Network'),'network-icon-visible'),
             (_('Trash'),'trash-icon-visible'),
             (_('Mounted volumes'),'volumes-visible')
        )
        for t,k in DT_l:
            if k in GS.list_keys():
                g=GSCheckButton(t,k,GS)
                vb.pack_start(g,False,False,1)
        c.update_cboxs()
        return True

