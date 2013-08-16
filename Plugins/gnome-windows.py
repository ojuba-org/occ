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
import os.path
from OjubaControlCenter.pluginsClass import PluginsClass
from OjubaControlCenter.gwidgets import resetButton, comboBox, hscale, fontButton, creatVBox

## NOTE: these global vars is loader validators
category = 'gnome'
caption = _('Windows')
description = _("Adjust windows settings")
priority = 45

class occPlugin(PluginsClass):
    def __init__(self,ccw):
        PluginsClass.__init__(self, ccw, caption, category, priority)
        self.GConf=ccw.GConf
        creatVBox(self, ccw, description, self.GioSettings) 

    def GioSettings(self, vb, ccw):
        P='org.gnome.shell.overrides'
        if not P in ccw.GSchemas_List: return False
        GS = ccw.GSettings(P)
        FD_l=( \
             (_('Windows button layout'),'button-layout'),
        )
        BTLayout_ls=[':close', ':minimize', ':maximize', ':minimize,close',
                     ':maximize,close', ':minimize,maximize', ':minimize,maximize,close',
                     'close:', 'minimize:', 'maximize:', 'minimize,close:',
                     'maximize,close:', 'minimize,maximize:', 'minimize,maximize,close:']
        for t,k in FD_l:
            if k in GS.list_keys():
                cb=comboBox(t,k,GS, BTLayout_ls)
                vb.pack_start(cb,False,False,1)
        P='org.gnome.desktop.wm.preferences'
        if not P in ccw.GSchemas_List: return False
        GS = ccw.GSettings(P)
        FD_l=( \
             #(_('Windows button layout'),'button-layout'),
             (_('Action on title bar double-click'),'action-double-click-titlebar'),
             (_('Action on title bar middle-click'),'action-middle-click-titlebar'),
             (_('Action on title bar right-click'),'action-right-click-titlebar'),
             (_('Window focus mode'),'focus-mode')
        )
        for t,k in FD_l:
            if k in GS.list_keys():
                cb=comboBox(t,k,GS, GS.get_range(k)[1])
                vb.pack_start(cb,False,False,1)
        return True
    
