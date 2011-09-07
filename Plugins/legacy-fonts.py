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
import sys, os, os.path
import re
from urllib import unquote
import shutil
from glob import glob
from OjubaControlCenter.widgets import InstallOrInactive, error
from OjubaControlCenter.pluginsClass import PluginsClass
class occPlugin(PluginsClass):
  __ch_re=re.compile(r'\\(0\d\d)')
  def __init__(self,ccw):
    PluginsClass.__init__(self, ccw,_('Fixing legacy fonts:'),'desktop',110)
    p=os.path.expanduser('~/.fonts/')
    if not os.path.exists(p): os.mkdir(p)
    vb=gtk.VBox(False,2)
    self.add(vb)
    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    l=gtk.Label(_('Some legacy fonts do not use any standard encoding.\nThis tool helps you to convert them to standard openType fonts.\nDrag and drop the files into the list then click convert.'))
    h.pack_start(l,False,False,2)
    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    self.files = gtk.ListStore(str,str,float,int,str) # fn, basename, percent, pulse, label
    self.files_ls=gtk.TreeView(self.files)
    scroll=gtk.ScrolledWindow()
    scroll.set_policy(gtk.POLICY_NEVER,gtk.POLICY_ALWAYS)
    scroll.add(self.files_ls)
    h.pack_start(scroll,True,True,2)
    self.__init_list()
    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    b=gtk.Button(stock=gtk.STOCK_CLEAR)
    b.connect('clicked', lambda *args: self.files.clear())
    h.pack_start(b,False,False,2)
    b=gtk.Button(stock=gtk.STOCK_CONVERT)
    b.connect('clicked', self.convert_cb)
    h.pack_start(b,False,False,2)
    h.pack_start(InstallOrInactive(self, _("Install FontForge"), _("FontForge is installed"), _("FontForge is a font editing tool"), ['fontforge']),False,False,2)

  def convert(self, f):
    b=os.path.join(os.path.dirname(sys.argv[0]),"legacy2opentype")
    return os.system("%s '%s'" % (b,f))

  def convert_cb(self, b):
    if not os.path.exists('/usr/bin/fontforge'):
      error("FontForge is not installed, please install it."); return
    for l in self.files:
      f=l[0]
      l[4]=_("Converting ...")
      gtk.main_iteration()
      while(gtk.events_pending()): gtk.main_iteration()
      r=self.convert(f)
      l[2]=100
      if r==0: l[4]=_("Done")
      else: l[4]=_("Skipped")
  
  def drop_data_cb(self, widget, dc, x, y, selection_data, info, t):
    for i in selection_data.get_uris():
      if i.startswith('file://'): f=unquote(i[7:]); self.files.append([f,os.path.basename(f),0,-1,_("Not started")])
      else: print "Protocol not supported in [%s]" % i
    dc.drop_finish (True, t);

  def __init_list(self):
    cells=[]
    cols=[]
    cells.append(gtk.CellRendererText())
    cols.append(gtk.TreeViewColumn(_('Files'), cells[-1], text=1))
    cols[-1].set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    cols[-1].set_resizable(True)
    cols[-1].set_expand(True)
    cells.append(gtk.CellRendererProgress())
    cols.append(gtk.TreeViewColumn('%', cells[-1], value=2,pulse=3,text=4))
    cols[-1].set_expand(False)
    self.files_ls.set_headers_visible(True)
    for i in cols: self.files_ls.insert_column(i, -1)
    self.targets_l=gtk.target_list_add_uri_targets()
    self.files_ls.drag_dest_set(gtk.DEST_DEFAULT_ALL, self.targets_l,(1<<5)-1)
    self.files_ls.connect('drag-data-received',self.drop_data_cb)

