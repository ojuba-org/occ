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
import re
from glob import glob
from OjubaControlCenter.widgets import info,error
from OjubaControlCenter.pluginsClass import PluginsClass

## NOTE: these global vars is loader validators
category = 'desktop'
caption = _('Samples icon:')
description = ''
priority = 50

class occPlugin(PluginsClass):
    desktop_re=re.compile(r"^\s*XDG_DESKTOP_DIR\s*=\s*(.*)\s*$", re.M)
    def __init__(self,ccw):
        PluginsClass.__init__(self, ccw, caption, category, priority)
        self.load()
        vb=Gtk.VBox(False,2)
        self.add(vb)
        h=Gtk.HBox(False,2); vb.pack_start(h,False,False,6)
        l=Gtk.Label(_('ojuba is shipped with samples. You may find an icon to samples on your desktop.'))
        h.pack_start(l,False,False,2)
        h=Gtk.HBox(False,2); vb.pack_start(h,False,False,6)
        b=Gtk.Button(_("Remove samples icon"))
        b.connect('clicked', self.rm_samples)
        h.pack_start(b,False,False,2)
        b=Gtk.Button(_("Recreate samples icon"))
        b.connect('clicked', self.mk_samples)
        h.pack_start(b,False,False,2)

    def load(self):
        self.oj_conf=os.path.expanduser("~/.ojuba-samples-configured")
        self.xdg_cfg=os.environ.get('XDG_CONFIG_HOME', os.path.expanduser("~/.config"))
        self.xdg_cfg_dirs=os.path.join(self.xdg_cfg,"user-dirs.dirs")
        try: cfg=open(self.xdg_cfg_dirs,"rt").read()
        except IOError: l=None
        else: l=self.desktop_re.findall(cfg)
        if l: desktop=os.path.expanduser(os.path.expandvars(l[-1])).replace('"','')
        else: desktop=os.path.expanduser("~/Desktop")
        self.oj_samples=os.path.join(desktop,"عيّنات")

    def rm_samples(self, b):
        if not os.path.exists(self.oj_samples):
            info(_('Samples icon already removed.'), self.ccw)
            return
        try: os.unlink(self.oj_samples)
        except OSError: error(_('Unable to remove samples icon.'), self.ccw); return
        info(_('Done.'), self.ccw)

    def mk_samples(self, b):
        try: os.unlink(self.oj_conf)
        except OSError: pass
        if os.path.exists('/etc/X11/xinit/xinitrc.d/zz-samples.sh'):
            os.system('bash /etc/X11/xinit/xinitrc.d/zz-samples.sh')
            info(_('Done.'), self.ccw)

