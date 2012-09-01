# -*- coding: utf-8 -*-
"""
Ojuba Control Center
Copyright © 2011, Ojuba.org <core@ojuba.org>

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
import re
from OjubaControlCenter.utils import cmd_out
from OjubaControlCenter.widgets import NiceButton, InstallOrInactive, wait, sure, info, error, sel_dir_dlg
from OjubaControlCenter.pluginsClass import PluginsClass

## NOTE: these global vars is loader validators
category = 'install'
caption = _('Local repository:')
description = _("Ojuba can create local rpository for you!")
priority = 8

class occPlugin(PluginsClass):
  repo_fn="/etc/yum.repos.d/local-occ.repo"
  tdir_re=re.compile('''[\s\t]*baseurl[\s\t]*=[\s\t]*file://(.*)''')
  def __init__(self,ccw):
    PluginsClass.__init__(self, ccw, caption, category, priority)
    self.tdir=self.get_repo_path_cb()
    vb=Gtk.VBox(False,2)
    self.add(vb)
    h=Gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    l=Gtk.Label(description)
    h.pack_start(l,False,False,2)
    
    h=Gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    b=Gtk.Button(_('Change directory'))
    b.connect('clicked', self.ch_dir_cb)
    h.pack_start(b, False,False,2)
    l=Gtk.Label(_("Repository directory:"))
    h.pack_start(l,False,False,2)
    self.repo_dir_l = l = Gtk.Label(self.tdir)
    h.pack_start(l,False,False,2)
    
    h=Gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    self.gen_info_c = c = Gtk.CheckButton(_("Generate local repository informations"))
    #c.set_active(True)
    c.connect("toggled", self.ch_apply_b_sens)
    h.pack_start(c, False,False,2)
    self.write_config_c = c = Gtk.CheckButton(_("Write local repository configuration"))
    #c.set_active(True)
    c.connect("toggled", self.ch_apply_b_sens)
    h.pack_start(c, False,False,2)
    
    h=Gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    self.apply_b = b = Gtk.Button(_('Create local repository'))
    b.connect('clicked', self.apply_cb)
    h.pack_start(b, False,False,2)
    self.ch_apply_b_sens()
    
    self.rm_repo_b = b = Gtk.Button(_('Remove local repository'))
    b.connect('clicked', self.rm_repo_cb)
    h.pack_end(b, False,False,2)
    self.ch_rm_repo_b_sens()
    
  def ch_rm_repo_b_sens(self, *b):
    self.rm_repo_b.set_sensitive(os.path.isfile(self.repo_fn))
    
  def ch_apply_b_sens(self, *b):
    s=(self.gen_info_c.get_active() or self.write_config_c.get_active()) and os.path.isdir(self.tdir)
    self.apply_b.set_sensitive(s)
        
  def ch_dir_cb(self, *b):
    tdir_dlg=sel_dir_dlg(self.ccw)
    if os.path.isdir(self.tdir):
      tdir_dlg.set_filename(self.tdir)
    if (tdir_dlg.run()==Gtk.ResponseType.ACCEPT):
      self.tdir = tdir_dlg.get_filename()
      tdir_dlg.hide()
      self.repo_dir_l.set_text(self.tdir)
    else:
      tdir_dlg.hide()
    return self.ch_apply_b_sens()
    
  def apply_cb(self, *b):
    if not os.path.isdir(self.tdir):
      return error(_("Select repository directory frist!"), self.ccw)
    dlg=wait(self.ccw)
    dlg.show_all()
    ret=False
    if self.gen_info_c.get_active():
      s=self.create_repo_cb(self.tdir)
      if s: dlg.hide(); return error(s, self.ccw)
      ret=True
    if self.write_config_c.get_active():
      if self.write_repo_cb(self.tdir) == '0': ret=True
      else: self.write_config_c.set_active(False)
    dlg.hide()
    if ret:info(_("Done!"), self.ccw)
    self.ch_rm_repo_b_sens()
    
  def get_repo_path_cb(self):
    fn=self.repo_fn
    if not os.path.isfile(fn): return 'None'
    l=open(self.repo_fn, 'r').read().strip()
    m=self.tdir_re.findall(l)[0]
    if m:return m
    return 'None'
    
  def create_repo_cb(self, tdir):
    return cmd_out('''createrepo "%s"''' %tdir)[1]
    
  def write_repo_cb(self, tdir):
    file_cont="""[local-occ]\nname=local-occ\nbaseurl=file://%s\nenabled=1\ngpgcheck=0\ncost=400\nskip_if_unavailable=1""" %tdir
    # FIXME: UnicodeEncodeError when writing arabic using mech
    #return self.ccw.mechanism('run', 'write_conf', self.repo_fn, file_cont)
    # instead 
    tfn=os.path.join(os.path.expanduser('~'), '.local-repo')
    open(tfn, 'wt+').write(file_cont)
    cmd='mv -f "%s" "%s"' %(tfn, self.repo_fn)
    return self.ccw.mechanism('run', 'system', cmd)
    
  def rm_repo_cb(self, *b):
    cmd='rm -f "%s"' %self.repo_fn
    s = self.ccw.mechanism('run', 'system', cmd)
    self.ch_rm_repo_b_sens()
    if s == 'NotAuth': return
    if s == '0': info(_("Done!"), self.ccw)
    else: error(_("unexpected return code, possible an error had occurred."), self.ccw)
