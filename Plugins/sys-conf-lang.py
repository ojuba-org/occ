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
import pwd, os
import ConfigParser
from OjubaControlCenter.widgets import LaunchOrInstall,info,error
from OjubaControlCenter.pluginsClass import PluginsClass

## NOTE: these global vars is loader validators
category = 'desktop'
caption = _('System Language:')
description = ''
priority = 10

## TODO: add more languages, add gdm language
class occPlugin(PluginsClass):
    conf = ConfigParser.ConfigParser()
    u = pwd.getpwuid(os.geteuid())[0]
    lang_fn = '/var/lib/AccountsService/users/%s' %u
    def __init__(self,ccw):
        PluginsClass.__init__(self, ccw, caption, category, priority)
        vb = Gtk.VBox(False,2)
        self.add(vb)
        h = Gtk.HBox(False,2); vb.pack_start(h,False,False,6)
        l = Gtk.Label(_('Select the default system language'))
        h.pack_start(l,False,False,2)
        h = Gtk.HBox(False,2); vb.pack_start(h,False,False,6)
        self.ar_b = b = Gtk.Button("العربية")
        b.connect('clicked', self.set_lang, "ar_EG.utf8")
        h.pack_start(b,False,False,2)
        self.fr_b = b = Gtk.Button("Frensh")
        b.connect('clicked', self.set_lang, "fr_FR.utf8")
        h.pack_start(b,False,False,2)
        self.en_b = b = Gtk.Button("English")
        b.connect('clicked', self.set_lang)
        h.pack_start(b,False,False,2)
        #h.pack_start(LaunchOrInstall(self, _('Other Language'), lang_fn, ['system-config-language']), False, False, 0)
        self.get_lang()

    def get_lang(self):
        #self.ar_b.set_sensitive(False)
        #self.fr_b.set_sensitive(False)
        #self.en_b.set_sensitive(False)
        
        lang = None
        
        self.conf.read(self.lang_fn)
        
        if self.conf.has_option("User", "Language"):
            lang = self.conf.get("User", "Language")
        
        if lang:
            self.ar_b.set_sensitive(not lang.startswith('ar_'))
            self.fr_b.set_sensitive(not lang.startswith('fr_'))
            self.en_b.set_sensitive(not lang.startswith('en_'))
        
        return lang

    def set_lang(self, w, nl="en_US.utf8"):
        ## setup  new config if config file not exist
        config = [('language', nl), ('xsession', 'gnome'), ('systemaccount', 'false')]
        ## change language if config file exist
        if self.conf.has_option("User", "Language"):
            self.conf.set("User", "Language", nl)
            config = self.conf.items("User")
            
        c_list = map(lambda (a, b):"%s=%s" %(a,b), config)
        c_text = "[User]\n%s\n" % "\n".join(c_list)

        self.ccw.mechanism('run','write_conf',self.lang_fn, c_text)
        return self.get_lang()
        
    
