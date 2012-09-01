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
import os
from widgets import sure, error
from utils import run_file_man

unavail_txt=_('This setting Unavailable ')
def setup_reset_button(widget):
    CanReset = False
    RL = _('Reset')
    try:
        widget.gs.connect("changed::"+widget.k, widget.update)
        CanReset = True
    except TypeError:
        widget.gs.notify_add(widget.k,widget.update, None)
    if CanReset:
        widget.rb = b = Gtk.Button(RL)
        b.set_size_request(70,-1)
        widget.rb.connect('clicked', widget.reset)
        widget.pack_end(widget.rb,False,False,0)
    else:
        b = Gtk.Label(RL)
        widget.pack_end(b,False,False,6)
        b.set_size_request(60,-1)
        
def not_installed(vb, ccw):
    h=Gtk.HBox(False,0)
    h.pack_start(Gtk.Label(_('Not installed')),False,False,0)
    vb.pack_start(h,False,False,6)
    
class comboBox(Gtk.HBox):
    def __init__(self,caption,k,gs, List, ccw=None):
        Gtk.HBox.__init__(self,False,0)
        self.gs=gs
        self.k=k
        self.List=List
        cb_list = Gtk.ListStore(str, str)
        self.cb = Gtk.ComboBox.new_with_model(cb_list)
        warp_width = 1
        if len(List) > 10:
            warp_width = len(List) / 10
            self.cb.set_wrap_width(warp_width)
        cell = Gtk.CellRendererText()
        self.cb.pack_start(cell, True)
        self.cb.add_attribute(cell, 'text', 0)
        self.build_list_cb(List)
        self.cb.connect('changed', self.set_gconf)
        self.cb.set_size_request(300,-1)
        self.pack_start(Gtk.Label(caption),False,False,0)
        setup_reset_button(self)
        self.pack_end(self.cb,False,False,0)
        try:
            self.update()
        except TypeError:
            self.set_sensitive(False)
            self.set_tooltip_text(unavail_txt)

    def build_list_cb(self, List):
        cb_list = self.cb.get_model()
        cb_list.clear()
        for i in List:
            #cb_list.append([i])
            cb_list.append([i.replace('_',' ').replace(':','').replace(',','+').capitalize(), i])
                
    def update(self,*args, **kw):
        v=self.gs.get_string(self.k)
        try: self.cb.set_active(self.List.index(v))
        except ValueError: pass

    def reset(self, *args):
        self.gs.reset(self.k)

    def set_gconf(self,*args):
        tree_iter = self.cb.get_active_iter()
        if not tree_iter: return
        gv = self.gs.get_string(self.k)
        tx, cv = self.cb.get_model()[tree_iter][:2]
        if gv == cv: return
        self.gs.set_string(self.k,cv)

class comboBoxWithFolder(comboBox):
    def __init__(self,caption,k,gs, List, btCap, target, ls_function, ccw=None):
        self.ccw=ccw
        comboBox.__init__(self,caption,k,gs, List)
        self.cb.set_size_request(250,-1)
        self.targetdir=target
        self.ls_function=ls_function
        bt=Gtk.Button(btCap)
        bt.connect('clicked', self.opendir_cb)
        bt.set_size_request(170,-1)
        self.pack_end(bt,False,False,0)
        bt=Gtk.Button(_('Refresh'))
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
                error('%s\n%s' % (_('Could not create folder'),self.targetdir), self.ccw)
                return False
        run_file_man(self.targetdir)
    
class fontButton(Gtk.HBox):
    def __init__(self,caption,k,gs, ccw=None):
        self.ccw=ccw
        Gtk.HBox.__init__(self,False,0)
        self.gs=gs
        self.k=k
        self.font=None
        self.fb = Gtk.Button('...')
        self.fb.connect('clicked', self.select_font)
        self.fb.set_size_request(300,-1)
        self.pack_start(Gtk.Label(caption),False,False,0)
        setup_reset_button(self)
        self.pack_end(self.fb,False,False,0)
        try:
            self.update()
        except TypeError:
            self.set_sensitive(False)
            self.set_tooltip_text(unavail_txt)

    def select_font(self, *w):
        d = Gtk.FontChooserDialog('Select Font', self.ccw)
        d.set_font(self.font)
        r = d.run()
        nf = d.get_font()
        d.destroy()

        if r != Gtk.ResponseType.OK: return
        self.font = nf
        self.fb.set_label(self.font)
        self.set_gconf()
        
    def update(self,*args, **kw):
        v=self.gs.get_string(self.k)
        if v!=self.font:
            self.font=v
            self.fb.set_label(v)

    def reset(self, *args):
        self.gs.reset(self.k)
    
    def set_gconf(self,*args):
        nv = self.font
        cv = self.gs.get_string(self.k)
        if nv == cv: return
        self.gs.set_string(self.k, nv)

class hscale(Gtk.HBox):
    def __init__(self,caption,k,gs, ccw=None):
        Gtk.HBox.__init__(self,False,0)
        self.gs=gs
        self.k=k
        self.scale = Gtk.HScale()
        self.scale.set_range(0.5,3.0)
        self.scale.set_value_pos(Gtk.PositionType.LEFT)
        self.scale.set_size_request(300, -1)
        self.scale.connect("format-value", self.set_gconf)
        self.pack_start(Gtk.Label(caption),False,False,0)
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
        nv = self.scale.get_value()
        cv = self.gs.get_double(self.k)
        if nv == cv: return
        self.gs.set_double(self.k, nv)

class GSCheckButton(Gtk.HBox):
    def __init__(self,caption,k,gs, ccw=None):
        Gtk.HBox.__init__(self)
        self.gs=gs
        self.k=k
        self.chkb = Gtk.CheckButton(caption)
        try:
            self.update()
        except TypeError:
            self.set_sensitive(False)
            self.set_tooltip_text(unavail_txt)
        self.chkb.connect('toggled',self.set_gconf)
        self.pack_start(self.chkb,True,True,1)
        setup_reset_button(self)
        
    def set_gconf(self,*args):
        nv = self.chkb.get_active()
        cv = self.gs.get_boolean(self.k)
        if nv == cv: return
        self.gs.set_boolean(self.k, nv)

    def update(self,*args, **kw):
        v=self.gs.get_boolean(self.k)
        if v!=self.chkb.get_active(): self.chkb.set_active(v)
    
    def reset(self, *args):
        self.gs.reset(self.k)
        
class mainGSCheckButton(GSCheckButton):
    def __init__(self, widget,caption,k,c, ccw=None):
        GSCheckButton.__init__(self,caption,k,c)
        self.Widget = widget
        self.chkb.connect('toggled',self.update_cboxs)
    
    def update_cboxs(self, *args):
        childs = self.Widget.get_children()
        for child in childs:
            if not child == self:
                child.set_sensitive(self.chkb.get_active())
        
class resetButton(Gtk.HBox):
    def __init__(self,vbox, ccw=None):
        self.ccw=ccw
        Gtk.HBox.__init__(self,False,0)
        self.b = b = Gtk.Button(_("Reset all"))
        b.connect("clicked", self.reset_cb,vbox)
        self.pack_end(b,False,False,0)
    
    def reset_cb(self, b, vb):
        if not sure(_('Are you sure?'), self.ccw): return
        childs = vb.get_children()
        for child in childs:
            try:
                if child and hasattr(child, 'rb'): child.reset()
            except AttributeError: print child

def creatVBox(parent, ccw, description, gsFuc=not_installed, nogsFunc=not_installed, resetBtton=True):
    vbox=Gtk.VBox(False,2)
    vb=Gtk.VBox(False,2)
    #FIXME: Toggle comment state for next 7 lines to disable expander 
    #expander=Gtk.Expander()
    #expander.add(vbox)
    #expander.set_label(description)
    #parent.add(expander)
    parent.add(vbox)
    h=Gtk.HBox(False,0)
    h.pack_start(Gtk.Label(_('Adjust desktop fonts')),False,False,0)
    vbox.pack_start(h,False,False,6)
    vbox.pack_start(vb,False,False,6)
    
    if not ccw.GSettings:
        nogsFunc(vb, ccw)
    else:
        if gsFuc(vb, ccw):
            vbox.pack_start(resetButton(vb, ccw),False,False,1)
        else:
            if resetBtton: not_installed(vb, ccw)
