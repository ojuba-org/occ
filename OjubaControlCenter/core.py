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
import os.path
import sys

try: from gi.repository import Gio
except ImportError: Gio=None

try: from gi.repository import GConf
except ImportError: GConf=None
gconf=None

if not GConf:
  try: import gconf
  except ImportError: pass

ld=os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])),'..','share','locale')
if not os.path.exists(ld): ld=os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])),'locale')
gettext.install('occ', ld, unicode=0)

import rpm
from gi.repository import Gtk

from OjubaControlCenter import loader
from OjubaControlCenter import categories
from OjubaControlCenter.pluginsClass import PluginsClass
from OjubaControlCenter.widgets import error, LaunchButton, CatFrame, MainButton, getSpecialIcon

from OjubaControlCenter.odbus.proxy.OCCBackend import Backend
import dbus
from dbus.mainloop.glib import DBusGMainLoop
bus = dbus.SessionBus()

  
class TabLabel(Gtk.HBox):
  def __init__(self, a):
    cat_id, caption, icon, tip=a
    l=Gtk.Label(caption)
    l.set_tooltip_text(tip)
    self.img=getSpecialIcon(icon) # Gtk.IconSize.BUTTON
    Gtk.HBox.__init__(self,False,0)
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
class OCCAbout(Gtk.AboutDialog):
  def __init__(self, parent):
    Gtk.AboutDialog.__init__(self, parent=parent)
    self.set_default_response(Gtk.ResponseType.CLOSE)
    #self.connect('delete-event', self.__hide_cb)
    #self.connect('response', self.__hide_cb)
    try: self.set_program_name("OCC")
    except: pass
    self.set_name(_("OCC"))
    #self.about_dlg.set_version(version)
    self.set_copyright("Copyright © 2009 ojuba.org")
    self.set_comments(_("Ojuba Control Center"))
    self.set_license("""\
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
    self.set_website("http://linux.ojuba.org")
    self.set_website_label("ojuba Linux web site")
    self.set_authors(["Muayyad Saleh Alsadi <alsadi@ojuba.org>", "Ehab El-Gedawy <ehabsas@gmail.com>"])
    self.run()
    self.destroy()
    
class CCWindow(Gtk.Window):
    
  def __init__(self):
    Gtk.Window.set_default_icon_name('ojuba-control-center')
    Gtk.Window.__init__(self)
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
    self.connect("delete_event", Gtk.main_quit)
    self.connect("destroy", Gtk.main_quit)
    self.set_size_request(750,650)
    self.set_title(_('Ojuba Control Center'))
    #self.maximize()
    self.set_resizable(False)
    self.set_position(Gtk.WindowPosition(1))
    
    vb=Gtk.VBox(False,2)
    self.add(vb)
    vb.show()
    
    h=Gtk.HBox(False,6); vb.pack_start(h,False,False,6)
    l=Gtk.Label()
    l.set_markup("""<span size="xx-large"><b>:::</b></span>""")
    
    self.GoMain_b = b = Gtk.Button()
    b.set_tooltip_markup("""<span size="large">%s</span>""" % (_("Back to Main")))
    b.add(l)
    b.set_focus_on_click(False)
    b.connect('clicked', self.show_main_cb)
    h.pack_start(b,False,False,6)
    
    #h.pack_start(Gtk.Image.new_from_icon_name('ojuba-control-center',Gtk.IconSize.DIALOG),False,False,6)
    #l=Gtk.Label()
    #l.set_markup("""<span size="large">%s</span>""" % (_("Ojuba Control Center")))
    b=Gtk.Button()
    b.add(Gtk.Image.new_from_icon_name('ojuba-control-center',Gtk.IconSize.DIALOG))
    b.set_tooltip_markup("""<span size="large">%s</span>""" % (_("About Ojuba Control Center")))
    #b.add(l)
    b.set_focus_on_click(False)
    b.connect('clicked', self.show_about_dlg)
    #h.pack_end(Gtk.Image.new_from_icon_name('ojuba-control-center',Gtk.IconSize.DIALOG),False,False,6)
    h.pack_end(b, False, False, 6)
    #h.pack_start(Gtk.Image.new_from_icon_name('start-here',Gtk.IconSize.DIALOG),False,False,6)
    h.show_all()
    self.GoMain_b.hide()
    
    
    # Main ScrolledWindow
    self.main_container = ms =Gtk.ScrolledWindow()
    ms.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
    vb.pack_start(ms, True, True, 6)
    
    # Main contianer
    mvb = Gtk.VBox(False,2)
    ms.add_with_viewport(mvb)
    ms.show_all()
    
    # Sub ScrolledWindow
    self.sub_container = ss = Gtk.ScrolledWindow()
    ss.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
    vb.pack_start(ss, True, True, 6)
    
    
    # Sub container
    svb = Gtk.VBox(False, 2)
    ss.add_with_viewport(svb)
    #ss.show()
    svb.show()
    
    self.vis_plugins = []
    self.cat_v={}
    self.cat_c={}
    self.cat_plugins={}
    #self.cat.connect('switch-page', self.__activate_page)
    for i in categories.ls:
        self.__newCat(i)
    skip=sum(map(lambda a: a[15:].split(','),
      filter(lambda s: s.startswith('--skip-plugins='), sys.argv[1:])),[])
    self.debug='--debug' in sys.argv[1:]
    self.__loadPlugins(skip)
    self.show()

  def show_about_dlg(self, *w):
    return OCCAbout(self)
    
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
  
  def __newCat(self,i):
    mvb = self.main_container.get_children()[0].get_children()[0]
    if type(i)==str:
      k = i
      r = CatFrame(i)
    else:
      k = i[0]
      r = CatFrame(*i)
    mvb.pack_start(r, False, False, 2)
    mvb.show_all()
    self.cat_v[k]=r
    self.cat_plugins[k]=[]
    return r
    #print mvb, svb
    
  def __newCat__old(self,i):
    if type(i)==str:
      k,t1,t2=i,i,''
      tl=Gtk.Label(i)
      icon=None
    else:
      k,t1,t2=i[0],i[1],i[3]
      tl=TabLabel(i)
      icon=getSpecialIcon(i[2])
    v=Gtk.VBox(False,2)
    s=Gtk.ScrolledWindow()
    r=Gtk.VBox(False,0)
    r = Gtk.Notebook()
    r.set_scrollable(True)
    r.set_show_border(True)
    r.popup_enable()
    l=Gtk.Label()
    l.set_markup('''<span size="xx-large" weight="bold">%s</span>\n<i>%s</i>''' % (t1,t2))
    s.set_policy(Gtk.PolicyType.AUTOMATIC,Gtk.PolicyType.AUTOMATIC)
    h=Gtk.HBox(False,2)
    if icon: h.pack_start(icon,False,False,2)
    h.pack_start(l,False,False,2)
    v.pack_start(h,False,False,2)
    v.pack_start(Gtk.HSeparator(),False,False,2)
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
    p=loader.loadPlugins(self.__pluginsDir,PluginsClass,'occPlugin',skip,self.debug,self)
    p.sort(lambda a,b: a.priority-b.priority)
    btncnt = dict((i[0],[0, Gtk.HBox(), False]) for i in categories.ls)
    svb = self.sub_container.get_children()[0].get_children()[0]
    #h=Gtk.HBox(False,2)
    for i in p:
      if i.category in btncnt:
        btncnt[i.category][0] += 1
      else:
        btncnt[i.category][0] = 0
      
      if btncnt[i.category][0] % 6 == 0:
        btncnt[i.category][1] = Gtk.HBox()
        btncnt[i.category][2] = False
        
      h = btncnt[i.category][1]
      if not btncnt[i.category][2]:
        btncnt[i.category][2] = True
        try: self.cat_v[i.category].pack_start(h,False,False,0)
        except KeyError: self.__newCat(i.category).pack_start(h,False,False,0)
        
      # pack main buttons
      h.pack_start(self.create_buttons(i),False,False,6)
      h.show_all()
      # pack plugin
      svb.pack_start(i,False,False,0)
      self.cat_plugins[i.category].append(i)
      
      
   
  def create_buttons(self, plugin):
    # we must remove char : in the caption ?
    caption = plugin.caption.replace(':', '')
    # FIXME: make fixed size main button widget
    b=MainButton(caption, icon='ojuba-control-center') #stock=Gtk.STOCK_PREFERENCES)
    b.set_tooltip_text(caption)
    b.connect('clicked', self.show_plugin, plugin)
    return b

  def show_plugin(self, b, plugin):
    for p in self.vis_plugins:
        p.hide()
    plugin.show_all()
    self.vis_plugins.append(plugin)
    self.GoMain_b.show_all()
    self.main_container.hide()
    self.sub_container.show()
  
  def show_main_cb(self, *b):
    self.GoMain_b.hide()
    self.sub_container.hide()
    self.main_container.show_all()
    for p in self.vis_plugins:
        p.hide()
    self.vis_plugins = []
    
def main():
  w=CCWindow()
  Gtk.main()

if __name__ == '__main__':
  main()


