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
import gtk
from widgets import sure, error
from utils import run_file_man
import os

unavail_txt=_('This setting Unavailable ')
def setup_reset_button(widget):
  CanReset = False
  RL = _('Reset')
  try:
    widget.gs.connect("changed::"+widget.k, widget.update)
    CanReset = True
  except TypeError:
    widget.gs.notify_add(widget.k, widget.update)
  #CanReset = True
  if CanReset:
    widget.rb = gtk.Button(RL)
    widget.rb.connect('clicked', widget.reset)
    widget.pack_end(widget.rb,False,False,0)
  else:
    widget.pack_end(gtk.Label(RL),False,False,6)

def not_installed(vb):
  h=gtk.HBox(False,0)
  h.pack_start(gtk.Label(_('Not installed')),False,False,0)
  vb.pack_start(h,False,False,6)
  
class comboBox(gtk.HBox):
  def __init__(self,caption,k,gs, List):
    gtk.HBox.__init__(self,False,0)
    self.gs=gs
    self.k=k
    self.List=List
    self.cb = gtk.ComboBox()
    cell = gtk.CellRendererText()
    self.cb.pack_start(cell)
    self.cb.add_attribute(cell, 'text', 0)
    self.build_list_cb(List)
    self.cb.connect('changed', self.set_gconf)
    self.cb.set_size_request(300,-1)
    self.pack_start(gtk.Label(caption),False,False,0)
    setup_reset_button(self)
    self.pack_end(self.cb,False,False,0)
    try:
      self.update()
    except TypeError:
      self.set_sensitive(False)
      self.set_tooltip_text(unavail_txt)

  def build_list_cb(self, List):
    cb_list = gtk.ListStore(str)
    self.cb.set_model(cb_list)
    for i in List:
      cb_list.append([i])
        
  def update(self,*args, **kw):
    v=self.gs.get_string(self.k)
    self.cb.set_active(self.List.index(v))
    
  def reset(self, *args):
    self.gs.reset(self.k)

  def set_gconf(self,*args):
    gv=self.gs.get_string(self.k)
    cv=self.cb.get_model().get_value(self.cb.get_active_iter(), 0)
    if gv != cv:
      self.gs.set_string(self.k,cv)

class comboBoxWithFolder(comboBox):
  def __init__(self,caption,k,gs, List, btCap, target, ls_function):
    comboBox.__init__(self,caption,k,gs, List)
    self.cb.set_size_request(250,-1)
    self.targetdir=target
    self.ls_function=ls_function
    bt=gtk.Button(btCap)
    bt.connect('clicked', self.opendir_cb)
    bt.set_size_request(170,-1)
    self.pack_end(bt,False,False,0)
    bt=gtk.Button(_('Refresh'))
    bt.connect('clicked', self.refresh_combo_cb)
    bt.set_size_request(80,-1)
    self.pack_end(bt,False,False,0)
  
  def refresh_combo_cb(self, b):
    self.List = List = self.ls_function()
    self.build_list_cb(List)
    self.update()
    
  def opendir_cb(self, b):
    if not os.path.isdir(self.targetdir):
      try:
        os.makedirs(self.targetdir)
      except OSError, e:
        print str(e)
        error('%s\n%s' % (_('Could not create folder'),self.targetdir))
        return False
    run_file_man(self.targetdir)
  
class fontButton(gtk.HBox):
  def __init__(self,caption,k,gs):
    gtk.HBox.__init__(self,False,0)
    self.gs=gs
    self.k=k
    self.fb = gtk.FontButton()
    self.fb.connect('font-set', self.set_gconf)
    self.fb.set_size_request(300,-1)
    self.pack_start(gtk.Label(caption),False,False,0)
    setup_reset_button(self)
    self.pack_end(self.fb,False,False,0)
    try:
      self.update()
    except TypeError:
      self.set_sensitive(False)
      self.set_tooltip_text(unavail_txt)

  def update(self,*args, **kw):
    v=self.gs.get_string(self.k)
    if v!=self.fb.get_font_name(): self.fb.set_font_name(v)
    
  def reset(self, *args):
    self.gs.reset(self.k)
  
  def set_gconf(self,*args):
    self.gs.set_string(self.k, self.fb.get_font_name())

class hscale(gtk.HBox):
  def __init__(self,caption,k,gs):
    gtk.HBox.__init__(self,False,0)
    self.gs=gs
    self.k=k
    self.scale = gtk.HScale()
    self.scale.set_range(0.5,3.0)
    self.scale.set_value_pos(gtk.POS_LEFT)
    self.scale.set_size_request(300, -1)
    self.scale.connect("format-value", self.set_gconf)
    self.pack_start(gtk.Label(caption),False,False,0)
    setup_reset_button(self)
    self.pack_end(self.scale,False,False,0)
    try:
      self.update()
    except TypeError:
      self.set_sensitive(False)
      self.set_tooltip_text(unavail_txt)

  def update(self,*args, **kw):
    v=self.gs.get_double(self.k)
    if v!=self.scale.get_value(): self.scale.set_value(v)
    
  def reset(self, *args):
    self.gs.reset(self.k)
    
  def set_gconf(self,*args):
    self.gs.set_double(self.k, self.scale.get_value())

class GSCheckButton(gtk.HBox):
  def __init__(self,caption,k,gs):
    gtk.HBox.__init__(self)
    self.gs=gs
    self.k=k
    self.chkb = gtk.CheckButton(caption)
    try:
      self.update()
    except TypeError:
      self.set_sensitive(False)
      self.set_tooltip_text(unavail_txt)
    self.chkb.connect('toggled',self.set_gconf)
    self.pack_start(self.chkb,True,True,1)
    setup_reset_button(self)
    
  def set_gconf(self,*args):
    self.gs.set_boolean(self.k, self.chkb.get_active())

  def update(self,*args, **kw):
    v=self.gs.get_boolean(self.k)
    if v!=self.chkb.get_active(): self.chkb.set_active(v)
  
  def reset(self, *args):
    self.gs.reset(self.k)
    
class mainGSCheckButton(GSCheckButton):
   def __init__(self, widget,caption,k,c):
     GSCheckButton.__init__(self,caption,k,c)
     self.widget = widget
     self.chkb.connect('toggled',self.update_cboxs)
   
   def update_cboxs(self, *args):
     childs = self.widget.get_children()
     for child in childs:
       if not child == self:
         child.set_sensitive(self.chkb.get_active())
     
class resetButton(gtk.HBox):
  def __init__(self,vbox):
    gtk.HBox.__init__(self,False,0)
    self.b = b = gtk.Button(_("Reset all"))
    b.connect("clicked", self.reset_cb,vbox)
    self.pack_end(b,False,False,0)
  
  def reset_cb(self, b, vb):
    if not sure(_('Are you sure?')): return
    childs = vb.get_children()
    for child in childs:
       try:
         if child and hasattr(child, 'rb'): child.reset()
       except AttributeError: print child

