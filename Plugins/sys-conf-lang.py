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
import re
from OjubaControlCenter.widgets import LaunchOrInstall,info,error
from OjubaControlCenter.pluginsClass import PluginsClass

## NOTE: these global vars is loader validators
category = 'desktop'
caption = _('System Language:')
description = ''
priority = 10

class occPlugin(PluginsClass):
    lang_re=re.compile(r'''^(\s*LANG\s*=\s*)['"]([^"']*)['"]''')
    lang_fn='/etc/sysconfig/i18n'
    def __init__(self,ccw):
        PluginsClass.__init__(self, ccw, caption, category, priority)
        vb=Gtk.VBox(False,2)
        self.add(vb)
        h=Gtk.HBox(False,2); vb.pack_start(h,False,False,6)
        l=Gtk.Label(_('Select the default system language'))
        h.pack_start(l,False,False,2)
        h=Gtk.HBox(False,2); vb.pack_start(h,False,False,6)
        self.ar_b = b = Gtk.Button("العربية")
        b.connect('clicked', self.set_lang, "ar_EG.UTF-8")
        h.pack_start(b,False,False,2)
        self.en_b = b = Gtk.Button("English")
        b.connect('clicked', self.set_lang)
        h.pack_start(b,False,False,2)
        h.pack_start(LaunchOrInstall(self,_('Other Language'),'/usr/bin/system-config-language',['system-config-language']),False,False,0)
        self.get_lang()

    def get_lang(self):
        try: lang=open(self.lang_fn, 'r').read().strip()
        except OSError: lang=""
        m=self.lang_re.search(lang)
        if m:
            self.ar_b.set_sensitive(not m.group(2).startswith('ar_'))
            self.en_b.set_sensitive(not m.group(2).startswith('en_'))
        return lang

    def set_lang(self, w, nl="en_US.UTF-8"):
        lang=self.get_lang()
        l,e=self.lang_re.subn(r'\1"%s"' %nl,lang)
        #print l,nl
        if e==0: l='''LANG="en_US.UTF-8"\nSYSFONT="latarcyrheb-sun16"'''
        self.ccw.mechanism('run','write_conf',self.lang_fn, l)
        self.get_lang()
        

