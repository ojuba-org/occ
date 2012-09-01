#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent syntax=python
# -*- Mode: Python; py-indent-offset: 4 -*-
"""
Ojuba Control Center
Copyright © 2009-2011, ojuba.org <core@ojuba.org>

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

try: from gi.repository import Gio
except ImportError: Gio=None

try: from gi.repository import GConf
except ImportError: GConf=None
gconf=None

if not GConf:
    try: import gconf
    except ImportError: pass

import rpm


from OjubaControlCenter.mainGUI import *
from OjubaControlCenter.widgets import error, LaunchButton, CatFrame, MainButton, getSpecialIcon

from OjubaControlCenter.odbus.proxy.OCCBackend import Backend
import dbus
from dbus.mainloop.glib import DBusGMainLoop
bus = dbus.SessionBus()

    

# /usr/bin/gpk-install-catalog myfile.catalog

#import dbus



# http://www.packagekit.org/gtk-doc/Transaction.html#Transaction::ProgressChanged

#from yum.callbacks import DownloadBaseCallback
# 
#class MyDownloadCallback(    DownloadBaseCallback ):
# 
#        def updateProgress(self,name,frac,fread,ftime):
#                '''
#                Update the progressbar
#                @param name: filename
#                @param frac: Progress fracment (0 -> 1)
#                @param fread: formated string containing BytesRead
#                @param ftime : formated string containing remaining or elapsed time
#                '''
#                pct = int( frac*100 )
#                print " %s : %s " % (name,pct)
# 
# 
#if __name__ == '__main__':
#        my = YumBase()
#        my.doConfigSetup()
#        dnlcb = MyDownloadCallback()
#        my.repos.setProgressBar( dnlcb )
#        for pkg in my.pkgSack:
#                print pkg.name

#yb = yum.YumBase()
#yb.install(name='somepackage')
#yb.remove(name='someotherpackage')
#yb.resolveDeps()
#yb.processTransaction()

        
class CCWindow(Gtk.Window):
        
    def __init__(self):
        Gtk.Window.set_default_icon_name('ojuba-control-center')
        Gtk.Window.__init__(self)
        self.connect("delete_event", Gtk.main_quit)
        self.connect("destroy", Gtk.main_quit)
        self.set_size_request(750, 550)
        self.set_title(_('Ojuba Control Center'))
        #self.maximize()
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition(1))
        
        dbus_loop = DBusGMainLoop(set_as_default=True)
        bus = dbus.SystemBus()
        self.GSettings=None
        if Gio and hasattr(Gio, 'Settings'):
            self.GSettings=Gio.Settings
            self.GSchemas_List=self.GSettings.list_schemas()
        self.GConf=None
        if GConf:
            self.GConf=[GConf.Client.get_default(), GConf.ClientPreloadType.PRELOAD_NONE]
        elif gconf:
            self.GConf=[gconf.client_get_default(), gconf.CLIENT_PRELOAD_NONE]
        self.__init_pk()
        try: self.__mechanism = Backend(bus = bus)
        except dbus.DBusException, e:
            error(_("Error loading DBus:\n\tRun (setenforce 0) as root to stop SELinux, and try again.\nNote: You can disable SELinux by running (sestop) as root."),self)
            print e
            sys.exit(1)
        
        self.__pk=None
        self.__pkc=None
        
        vb = GUI(self)
        self.add(vb)
        self.show()

    def __init_pk(self):
        global bus
        self.__nopk=False
        try:
            self.__pk_proxy = bus.get_object('org.freedesktop.PackageKit', '/org/freedesktop/PackageKit')
            self.__pk_iface = dbus.Interface(self.__pk_proxy, 'org.freedesktop.PackageKit.Modify')
        except dbus.DBusException, e:
            self.__nopk=True

    def install_packages(self,pkgs,upgrade=1):
        if not pkgs or self.__nopk: return
        # options are show/hide-*: confirm-search confirm-deps confirm-install progress finished warning
        try: r=self.__pk_iface.InstallPackageNames(dbus.UInt32(0),pkgs,"hide-confirm-search,show-confirm-install,show-progress,show-finished")
        except dbus.DBusException, e: return -1
        return r

    def install_by_file(self,f):
        if not f or self.__nopk: return
        if type(f)!=list: l=[f]
        else: l=f
        try: r=self.__pk_iface.InstallProvideFiles(dbus.UInt32(0), pkgs, "hide-confirm-search,show-confirm-install,show-progress,show-finished")
        except dbus.DBusException, e: return -1
        return r

    def is_installed(self, pkgs):
        ts = rpm.TransactionSet()
        for p in pkgs:
            if not ts.dbMatch('name',p).count(): return False
        return True
    
    def installed_info(self, pkg):
        ts = rpm.TransactionSet()
        r = ts.dbMatch('name',pkg)
        if not r: return None
        return r.next()
        
    def mechanism(self,*args, **kw):
        try: return self.__mechanism.call(args)
        except dbus.exceptions.DBusException, msg:
            if kw.has_key('on_fail'): return kw['on_fail']
            if 'NotAuthorizedException' in str(msg): return 'NotAuth'
            raise
    def __activate_page(self,cat,p,n):
        if not self.cat_c.has_key(n): return
        for i in self.cat_plugins[self.cat_c[n]]: i._activate()
        # todo tell all plugins in this page we are active
        return True
    
def main():
    w=CCWindow()
    Gtk.main()

if __name__ == '__main__':
    main()


