#!/usr/bin/python
# -*- coding: utf-8 -*-
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
import gettext
import os
import os.path
import sys
import glob
import imputil
try: from gi.repository import Gio
except ImportError: Gio=None
ld=os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])),'..','share','locale')
if not os.path.exists(ld): ld=os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])),'locale')
gettext.install('occ', ld, unicode=0)

import rpm
import gtk
import gtk.gdk


from OjubaControlCenter import loader
from OjubaControlCenter import categories
from OjubaControlCenter.pluginsClass import PluginsClass
from OjubaControlCenter.widgets import error, LaunchButton

from OjubaControlCenter.odbus.proxy.OCCBackend import Backend
import dbus
from dbus.mainloop.glib import DBusGMainLoop
bus = dbus.SessionBus()

def getSpecialIcon(icon,size=gtk.ICON_SIZE_DIALOG):
  return gtk.image_new_from_icon_name(icon, size)
  
class TabLabel(gtk.HBox):
  def __init__(self, a):
    cat_id, caption, icon, tip=a
    l=gtk.Label(caption)
    l.set_tooltip_text(tip)
    self.img=getSpecialIcon(icon) # gtk.ICON_SIZE_BUTTON
    gtk.HBox.__init__(self,False,0)
    self.set_border_width(0)
    self.pack_start(self.img,False,False,0)
    self.pack_start(l,True,True,0)
    self.show_all()

# /usr/bin/gpk-install-catalog myfile.catalog

#import dbus



# http://www.packagekit.org/gtk-doc/Transaction.html#Transaction::ProgressChanged

#from yum.callbacks import DownloadBaseCallback
# 
#class MyDownloadCallback(  DownloadBaseCallback ):
# 
#    def updateProgress(self,name,frac,fread,ftime):
#        '''
#        Update the progressbar
#        @param name: filename
#        @param frac: Progress fracment (0 -> 1)
#        @param fread: formated string containing BytesRead
#        @param ftime : formated string containing remaining or elapsed time
#        '''
#        pct = int( frac*100 )
#        print " %s : %s " % (name,pct)
# 
# 
#if __name__ == '__main__':
#    my = YumBase()
#    my.doConfigSetup()
#    dnlcb = MyDownloadCallback()
#    my.repos.setProgressBar( dnlcb )
#    for pkg in my.pkgSack:
#        print pkg.name

#yb = yum.YumBase()
#yb.install(name='somepackage')
#yb.remove(name='someotherpackage')
#yb.resolveDeps()
#yb.processTransaction()


class CCWindow(gtk.Window):
  def __init__(self):
    gtk.window_set_default_icon_name('ojuba-control-center')
    gtk.Window.__init__(self)
    dbus_loop = DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    self.GSettings=None
    if Gio and hasattr(Gio, 'Settings'): self.GSettings=Gio.Settings
    self.__init_about_dialog()
    self.__init_pk()
    self.__mechanism = Backend(bus = bus)
    self.__pk=None
    self.__pkc=None
    self.connect("delete_event", gtk.main_quit)
    self.set_size_request(800,400)
    self.set_title(_('Ojuba Control Center'))
    self.maximize()
    vb=gtk.VBox(False,2)
    self.add(vb)
    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    h.pack_start(gtk.image_new_from_icon_name('ojuba-control-center',gtk.ICON_SIZE_DIALOG),False,False,6)
    l=gtk.Label()
    l.set_markup("""<span size="xx-large">%s</span>""" % (_("Ojuba Control Center")))
    b=gtk.Button()
    b.add(l)
    b.connect('clicked', lambda b: self.about_dlg.show_all())
    h.pack_start(b,True,False,6)
    h.pack_start(gtk.image_new_from_icon_name('start-here',gtk.ICON_SIZE_DIALOG),False,False,6)
    self.cat=gtk.Notebook()
    vb.pack_start(self.cat,True,True,6)
    self.cat.set_tab_pos(gtk.POS_LEFT)
    self.cat.set_scrollable(True)
    self.cat_v={}
    self.cat_c={}
    self.cat_plugins={}
    self.cat.connect('switch-page', self.__activate_page)
    for i in categories.ls: self.__newCat(i)
    skip=sum(map(lambda a: a[15:].split(','),
      filter(lambda s: s.startswith('--skip-plugins='), sys.argv)),[])
    self.__loadPlugins(skip)
    self.show_all()
    gtk.main()

  def __hide_cb(self, w, *args): w.hide(); return True

  def __init_about_dialog(self):
    self.about_dlg=gtk.AboutDialog()
    self.about_dlg.set_default_response(gtk.RESPONSE_CLOSE)
    self.about_dlg.connect('delete-event', self.__hide_cb)
    self.about_dlg.connect('response', self.__hide_cb)
    try: self.about_dlg.set_program_name("OCC")
    except: pass
    self.about_dlg.set_name(_("OCC"))
    #self.about_dlg.set_version(version)
    self.about_dlg.set_copyright("Copyright © 2009 ojuba.org")
    self.about_dlg.set_comments(_("Ojuba Control Center"))
    self.about_dlg.set_license("""\
    Released under terms of Waqf Public License.
    This program is free software; you can redistribute it and/or modify
    it under the terms of the latest version Waqf Public License as
    published by Ojuba.org.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

    The Latest version of the license can be found on
    "http://waqf.ojuba.org/"
""")
    self.about_dlg.set_website("http://linux.ojuba.org")
    self.about_dlg.set_website_label("ojuba Linux web site")
    self.about_dlg.set_authors(["Muayyad Saleh Alsadi <alsadi@ojuba.org>", "Ehab El-Gedawy <ehabsas@gmail.com>"])

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
    
  def __newCat(self,i):
    if type(i)==str:
      k,t1,t2=i,i,''
      tl=gtk.Label(i)
      icon=None
    else:
      k,t1,t2=i[0],i[1],i[3]
      tl=TabLabel(i)
      icon=getSpecialIcon(i[2])
    v=gtk.VBox(False,2)
    s=gtk.ScrolledWindow()
    r=gtk.VBox(False,0)
    l=gtk.Label()
    l.set_markup('''<span size="xx-large" weight="bold">%s</span>\n<i>%s</i>''' % (t1,t2))
    s.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_ALWAYS)
    h=gtk.HBox(False,2)
    if icon: h.pack_start(icon,False,False,2)
    h.pack_start(l,False,False,2)
    v.pack_start(h,False,False,2)
    v.pack_start(gtk.HSeparator(),False,False,2)
    v.pack_start(s,True,True,0)
    n=self.cat.append_page(v, tl)
    self.cat_v[k]=r
    self.cat_c[n]=k
    self.cat_plugins[k]=[]
    s.add_with_viewport(r)
    return r

  def __loadPlugins(self,skip):
    self.__exeDir=os.path.abspath(os.path.dirname(sys.argv[0]))
    self.__pluginsDir=os.path.join(self.__exeDir,'Plugins')
    if not os.path.isdir(self.__pluginsDir):
      self.__pluginsDir=os.path.join(self.__exeDir,'..','share','occ','Plugins')
    p=loader.loadPlugins(self.__pluginsDir,PluginsClass,'occPlugin',skip,self)
    p.sort(lambda a,b: a.priority-b.priority)
    for i in p:
      try: self.cat_v[i.category].pack_start(i,False,False,0)
      except KeyError: self.__newCat(i.category).pack_start(i,False,False,0)
      self.cat_plugins[i.category].append(i)

def main():
  try: w=CCWindow()
  except KeyboardInterrupt: print 'Keyboard interrupt!, Exiting...'

if __name__ == '__main__':
  main()

