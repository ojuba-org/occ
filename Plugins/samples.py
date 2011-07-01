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
import os, os.path
import re
from glob import glob
from OjubaControlCenter.widgets import info,error
from OjubaControlCenter.pluginsClass import PluginsClass

class occPlugin(PluginsClass):
  desktop_re=re.compile(r"^\s*XDG_DESKTOP_DIR\s*=\s*(.*)\s*$", re.M)
  def __init__(self,ccw):
    PluginsClass.__init__(self, ccw,_('Samples icon:'),'desktop', 50)
    self.load()
    vb=gtk.VBox(False,2)
    self.add(vb)
    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    l=gtk.Label(_('ojuba is shipped with samples. You may find an icon to samples on your desktop.'))
    h.pack_start(l,False,False,2)
    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    b=gtk.Button(_("Remove samples icon"))
    b.connect('clicked', self.rm_samples)
    h.pack_start(b,False,False,2)
    b=gtk.Button(_("Recreate samples icon"))
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
      info(_('Samples icon already removed.'))
      return
    try: os.unlink(self.oj_samples)
    except OSError: error(_('Unable to remove samples icon.')); return
    info(_('Done.'))

  def mk_samples(self, b):
    try: os.unlink(self.oj_conf)
    except OSError: pass
    if os.path.exists('/etc/X11/xinit/xinitrc.d/zz-samples.sh'):
      os.system('bash /etc/X11/xinit/xinitrc.d/zz-samples.sh')
      info(_('Done.'))

