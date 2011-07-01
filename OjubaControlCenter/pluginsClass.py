# -*- coding: utf-8 -*-
"""
Ojuba Control Center
Copyright © 2009, Muayyad Alsadi <alsadi@ojuba.org>

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
class PluginsClass(gtk.Frame):
  def __init__(self, ccw, caption, category, priority=100):
    self.ccw=ccw
    self.caption=caption
    self.category=category
    self.priority=priority
    self.activate_ls=[]
    self.load_ls=[]
    self.loaded=False
    gtk.Frame.__init__(self,caption)
    self.set_border_width(6)
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
