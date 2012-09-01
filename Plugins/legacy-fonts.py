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
import os
import sys
import re
from urllib import unquote
from glob import glob
from OjubaControlCenter.widgets import InstallOrInactive, error
from OjubaControlCenter.pluginsClass import PluginsClass

## NOTE: these global vars is loader validators
category = 'desktop'
caption = _('Fixing legacy fonts:')
description = _('Some legacy fonts do not use any standard encoding.\nThis tool helps you to convert them to standard openType fonts.\nDrag and drop the files into the list then click convert.')
priority = 110

class occPlugin(PluginsClass):
    __ch_re=re.compile(r'\\(0\d\d)')
    def __init__(self,ccw):
        PluginsClass.__init__(self, ccw, caption, category, priority)
        p=os.path.expanduser('~/.fonts/')
        if not os.path.exists(p): os.mkdir(p)
        vb=Gtk.VBox(False,2)
        self.add(vb)
        h=Gtk.HBox(False,2); vb.pack_start(h,False,False,6)
        l=Gtk.Label(description)
        h.pack_start(l,False,False,2)
        h=Gtk.HBox(False,2); vb.pack_start(h,False,False,6)
        self.files = Gtk.ListStore(str,str,float,int,str) # fn, basename, percent, pulse, label
        self.files_ls=Gtk.TreeView(self.files)
        scroll=Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER,Gtk.PolicyType.ALWAYS)
        scroll.add(self.files_ls)
        h.pack_start(scroll,True,True,2)
        self.__init_list()
        h=Gtk.HBox(False,2); vb.pack_start(h,False,False,6)
        b=Gtk.Button(stock=Gtk.STOCK_CLEAR)
        b.connect('clicked', lambda *args: self.files.clear())
        h.pack_start(b,False,False,2)
        b=Gtk.Button(stock=Gtk.STOCK_CONVERT)
        b.connect('clicked', self.convert_cb)
        h.pack_start(b,False,False,2)
        h.pack_start(InstallOrInactive(self, _("Install FontForge"), _("FontForge is installed"), _("FontForge is a font editing tool"), ['fontforge']),False,False,2)

    def convert(self, f):
        b=os.path.join(os.path.dirname(sys.argv[0]),"legacy2opentype")
        return os.system("%s '%s'" % (b,f))

    def convert_cb(self, b):
        if not os.path.exists('/usr/bin/fontforge'):
            error("FontForge is not installed, please install it.", self.ccw); return
        for l in self.files:
            f=l[0]
            l[4]=_("Converting ...")
            Gtk.main_iteration()
            while(Gtk.events_pending()): Gtk.main_iteration()
            r=self.convert(f)
            l[2]=100
            if r==0: l[4]=_("Done")
            else: l[4]=_("Skipped")
    
    def drop_data_cb(self, widget, dc, x, y, selection_data, info, t):
        for i in selection_data.get_uris():
            if i.startswith('file://'):
             f=unquote(i[7:])
             self.files.append([f,os.path.basename(f),float(0),-1,_("Not started")])
            else: print "Protocol not supported in [%s]" % i
        #dc.drop_finish (True, t);

    def __init_list(self):
        cells=[]
        cols=[]
        cells.append(Gtk.CellRendererText())
        cols.append(Gtk.TreeViewColumn(_('Files'), cells[-1], text=1))
        cols[-1].set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        cols[-1].set_resizable(True)
        cols[-1].set_expand(True)
        cells.append(Gtk.CellRendererProgress())
        cols.append(Gtk.TreeViewColumn('%', cells[-1], value=2,pulse=3,text=4))
        cols[-1].set_expand(False)
        self.files_ls.set_headers_visible(True)
        for i in cols: self.files_ls.insert_column(i, -1)
        self.targets_l=Gtk.TargetList.new([])
        self.targets_l.add_uri_targets((1<<5)-1)
        self.files_ls.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)
        self.files_ls.drag_dest_set_target_list(self.targets_l)
        self.files_ls.connect('drag-data-received',self.drop_data_cb)

