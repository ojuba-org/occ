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
from gi.repository import Gtk, Gdk
class PluginsClass(Gtk.Frame):
    def __init__(self, ccw, caption, category, priority=100):
        self.ccw=ccw
        self.caption=caption
        self.category=category
        self.priority=priority
        self.activate_ls=[]
        self.load_ls=[]
        self.loaded=False
        Gtk.Frame.__init__(self)
        self.set_label(caption)
        self.set_border_width(6)
        #self.show_boarder=True
        self.set_shadow_type(Gtk.ShadowType(1))
        #self.modify_bg(Gtk.StateType(0),Gdk.Color(255,0,0))
        #rc=Gtk.RcStyle()
        #self.modify_style(rc)
        #for i in rc.base:
        #    i.red=255
        self.set_shadow_type(Gtk.ShadowType.IN)
        l=Gtk.Label(caption)
        l.set_markup('<span color="blue">%s</span>' %caption)
        self.set_label_widget(l)
        
    def _load(self):
        self.load()
        self.loaded=True
        for f in self.load_ls: f()
        self.activate()
        for f in self.activate_ls: f()
    def _activate(self):
        if self.loaded:
            self.activate()
            for f in self.activate_ls: f()
        else: self._load()

    def load(self):
        """The page containing the plugin is activated for the first time.
This method should be overridden."""
        pass
    def activate(self):
        """The page containing the plugin is activated.
This method should be overridden."""
        pass
