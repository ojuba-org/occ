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
import pwd
from OjubaControlCenter.pluginsClass import PluginsClass
from OjubaControlCenter.widgets import info, error


## NOTE: these global vars is loader validators
category = 'desktop'
caption = _('Graphical Login Manager')
## NOTE: we can use discription in main plugin label, to help search
description = _("Display Manager is the application that allow you to log into your desktop.\nIt's the application that might ask you to authenticate with your username and password")
priority = 150

class occPlugin(PluginsClass):
    dm_re=re.compile(r'''^\s*DISPLAYMANAGER\s*=\s*['"]?([^'"]+)['"]?\s*$''',re.M)
    def __init__(self,ccw):
        PluginsClass.__init__(self, ccw, caption, category, priority)
        vb=Gtk.VBox(False,2)
        self.add(vb)
        hb=Gtk.HBox(False,2); vb.pack_start(hb,True,True,6)
        l=Gtk.Label(description) # using discription here 
        #l.set_line_wrap(True)
        hb.pack_start(l,False,False,2)
        hb=Gtk.HBox(False,2); vb.pack_start(hb,True,True,2)
        self.dm_ls=['gdm','kdm','wdm','xdm', 'lxdm']
        self.dm_ls=filter(lambda i: os.path.exists('/usr/sbin/'+i) or os.path.exists('/usr/bin/'+i),self.dm_ls)
        self.dm=Gtk.ComboBoxText()
        for i in self.dm_ls: self.dm.append_text(i)
        self.dm.set_active(self.get_current())
        hb.pack_start(Gtk.Label(_("Available display managers:")),False,False,2)
        hb.pack_start(self.dm,False,False,2)
        b=Gtk.Button(_("save change"))
        b.connect('clicked',self.set_dm)
        hb.pack_start(b,False,False,2)
        hb=Gtk.HBox(False,2); vb.pack_start(hb,True,True,2)
        b=Gtk.Button(_('Enable Automatic Login as this user'))
        b.connect('clicked',self.autologin_cb)
        hb.pack_start(b,False,False,2)
        b=Gtk.Button(_('Disable Automatic Login'))
        b.connect('clicked',self.no_autologin_cb)
        hb.pack_start(b,False,False,2)

    def get_current(self):
        v=''
        if os.path.exists("/etc/sysconfig/desktop"):
            try: l=open("/etc/sysconfig/desktop","rt").read()
            except IOError: v=''
            else:
                try: v=self.dm_re.findall(l)[-1].strip()
                except IndexError: v=''
        if not v:
            if os.path.exists("/usr/sbin/gdm") or os.path.exists("/usr/bin/gdm"): v='gdm'
            elif os.path.exists("/usr/bin/kdm") or os.path.exists("/usr/sbin/kdm"): v='kdm'
            else: return 0
        v=v.lower()
        if v=='gnome': v='gdm'
        elif v=='kde': v='kdm'
        try: return self.dm_ls.index(v)
        except ValueError: return 0

    def set_dm(self,*args):
        s=''
        if os.path.exists("/etc/sysconfig/desktop"):
            s=self.ccw.mechanism('run','system', 'rm -f /etc/sysconfig/desktop')
        if s == 'NotAuth': return
        i=self.dm_ls[self.dm.get_active()]
        s=self.set_sysconf_disktop(i)
        if s == 'NotAuth': return
        if i != 'lxdm':
            s=self.ccw.mechanism('run','system', 'system-switch-displaymanager "%s"' % i)
        if s == 'NotAuth': return
        if s=='0': info(_('Display manager is now set to %s') % i, self.ccw)
        else: error(_('Unable to set display managed.'), self.ccw)

    def set_sysconf_disktop(self, dm):
        dm_txt='''DISPLAYMANAGER="%s"''' %dm
        print dm_txt
        s=self.ccw.mechanism('run','write_conf', '/etc/sysconfig/desktop', dm_txt)
        return s
        
    def autologin_cb(self, *args):
        u=pwd.getpwuid(os.geteuid())[0]
        s=self.ccw.mechanism('dm','enable_autologin', u)
        if s == 'NotAuth': return
        if s.startswith('-'): error(_('could not set automatic login in %s') % s[1:], self.ccw)
        elif s: info(_('Automatic login as %s was set in %s') % (u,s), self.ccw)
        else: error(_('could not set automatic login'), self.ccw)


    def no_autologin_cb(self, *args):
        s=self.ccw.mechanism('dm','disable_autologin')
        if s == 'NotAuth': return
        if not s: error(_('could not disable automatic login'), self.ccw)
        elif s.startswith('-'): error(_('could not disable automatic login in %s') % s[1:], self.ccw)
        else: info(_('automatic login is now disabled'), self.ccw)
        



