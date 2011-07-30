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
import pango
import os, os.path
import re
import shutil
from glob import glob
from OjubaControlCenter.widgets import wait, info, sure, error
from OjubaControlCenter.pluginsClass import PluginsClass

import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
dbus_loop = DBusGMainLoop(set_as_default = True)
bus = dbus.SystemBus()
interface = 'org.freedesktop.UDisks'

class occPlugin(PluginsClass):
  __dev_re=re.compile(r'(\d+)$')
  def __init__(self,ccw):
    self.__dev = bus.get_object(interface, "/org/freedesktop/UDisks")
    PluginsClass.__init__(self, ccw,_('LiveUSB'),'install', 150)
    vb=gtk.VBox(False,2)
    self.add(vb)
    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    l=gtk.Label(_('A Live System enables you to carry your operating system with you.\nAlso, You may add persistent layer so that it can hold your modification to the system.'))
    h.pack_start(l,False,False,2)
    hb=gtk.HBox(False,2); vb.pack_start(hb,False,False,6)
    hb.pack_start(gtk.Label(_('Source:')), False,False,2)
    self.src_iso_file=gtk.RadioButton(label=_('from iso file'))
    hb.pack_start(self.src_iso_file, False,False,2)
    h=gtk.HBox(False,2); hb.pack_start(h,False,False,2)
    self.iso_file_b=gtk.FileChooserButton(_('Choose live iso file'))
    h.pack_start(self.iso_file_b, False,False,2)
    self.src_iso_file.connect('toggled', lambda b: self.iso_file_b.set_sensitive(b.get_active()))
    
    self.src_iso_dev=gtk.RadioButton(self.src_iso_file, label=_('from CD/DVD device'))
    hb.pack_start(self.src_iso_dev, False,False,2)
    self.src_iso_dev_h=h=gtk.HBox(False,2); hb.pack_start(h,False,False,2)
    self.src_iso_dev.connect('toggled', lambda b: self.src_iso_dev_h.set_sensitive(b.get_active()))
    self.iso_dev_ls=gtk.combo_box_new_text()
    h.pack_start(self.iso_dev_ls, False,False,2)
    b=gtk.Button(stock=gtk.STOCK_REFRESH)
    b.connect('clicked', self.refresh_src_dev)
    h.pack_start(b, False,False,2)
    self.src_iso_dev.set_active(True)
    self.src_iso_file.set_active(True)

    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    h.pack_start(gtk.Label(_('Target Device:')), False,False,2)
    self.target_dev_ls=gtk.combo_box_new_text()
    h.pack_start(self.target_dev_ls, True,True,2)
    b=gtk.Button(stock=gtk.STOCK_REFRESH)
    b.connect('clicked', self.refresh_target_dev)
    h.pack_start(b, False,False,2)

    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    h.pack_start(gtk.Label(_('Target Options:')), False,False,2)
    self.format=gtk.CheckButton(_('Format target partition'))
    self.format.set_tooltip_text(_('uncheck this button to preserve data on target device'))
    h.pack_start(self.format, False,False,2)
    self.reset_mbr=gtk.CheckButton(_('Reset MBR'))
    self.reset_mbr.set_active(True)
    h.pack_start(self.reset_mbr, False,False,2)
    h.pack_start(gtk.Label(_('Overlay size:')), False,False,2)
    self.overlay_size=gtk.SpinButton()
    self.overlay_size.set_tooltip_text(_('size of persistent overlay in MB, 0 to disable'))
    self.overlay_size.get_adjustment().set_all(200, 0, 10240, 10, 0, 0)
    h.pack_start(self.overlay_size, False,False,2)
    h.pack_start(gtk.Label(_('MB')), False,False,0)
#    TODO: all the below options needs interaction to enter the pass-phrase
#    h.pack_start(gtk.Label('Home image size:'), False,False,2)
#    self.home_size=gtk.SpinButton()
#    self.home_size.set_tooltip_text(_('size of home image in MB, 0 to use the overlay'))
#    self.home_size.set_range(0,10240)
#    self.home_size.set_value(0)
#    h.pack_start(self.home_size, False,False,2)
#    self.home_enc=gtk.CheckButton(_('encrypted'))
#    self.home_enc.set_tooltip_text(_('Encrypt Home image'))
    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    b=gtk.Button(stock=gtk.STOCK_EXECUTE)
    b.connect('clicked', self.execute)
    h.pack_start(b, False,False,2)
    h.pack_start(gtk.Label(_("This will take some time.")), False,False,2)

    ff=gtk.FileFilter(); ff.add_pattern('*.[Ii][Ss][Oo]')
    self.iso_file_b.set_filter(ff)
    self.refresh_src_dev()
    self.refresh_target_dev()
  
  def dst_parse(self, target):
    if not target or ':' not in target: return None,0,None
    r=target.split(':',1)
    dst=r[0]
    s,l=r[1].split(' ',1)
    return dst,s,l

  def execute(self, *args):
    f="/usr/bin/livecd-iso-to-disk"
    if not os.path.exists(f): f="/mnt/live/LiveOS/livecd-iso-to-disk"
    if not os.path.exists(f):
      error(_("The package 'livecd-tools' is not installed."))
      if sure(_("Would you like to install 'livecd-tools'?")):
        self.ccw.install_packages(['livecd-tools'])
        info("Please try again.")
      return
    ov=self.overlay_size.get_value()
    opt="--noverify"
    dst,s,l=self.dst_parse(self.target_dev_ls.get_active_text())
    if not dst: error(_('Please choose valid target device.')); return

    if self.format.get_active():
      opt+=" --format"
      if not sure(_("Are you sure you want to format target device (labeled %s)?") % l): return
    if self.reset_mbr.get_active(): opt+=" --reset-mbr"
    if ov>0: opt+=" --overlay-size-mb %i" % ov
    
    if self.src_iso_file.get_active():
      src=self.iso_file_b.get_filename()
      if not src or not os.path.exists(src) or not src.lower().endswith('.iso'):
        error(_('Please choose a valid iso file')); return
    else:
      src=self.iso_dev_ls.get_active_text()
      if not src:
        error(_('Please choose a source device.')); return
    os.system("umount '%s'" % dst)
    cmd='''%s %s "%s" "%s"''' % (f, opt,src,dst)
    print cmd
    dlg=wait()
    p=self.__dev_re.findall(dst)[0]
    dst0=self.__dev_re.sub('',dst)
    self.ccw.mechanism('run','system','''echo ",,,*" | sfdisk %s -N%s''' % (dst0, p))
    while(gtk.main_iteration_do()): pass
    r=self.ccw.mechanism('run','system',cmd, on_fail='0')
    if r!='0': error(_("An error occurred while creating the live system.\nYou may run the following command in terminal to see the error:\n%s") % cmd)
    while(gtk.main_iteration_do()): pass
    dlg.hide()
    if dlg: dlg.destroy()

  def get_device_property(self, udi, key):
    dev=bus.get_object(interface, udi)
    return dev.Get(interface+'.Device', key, dbus_interface="org.freedesktop.DBus.Properties")

  def refresh_src_dev(self, *args):
    n=0
    l=self.__dev.EnumerateDevices(dbus_interface = interface)
    self.iso_dev_ls.get_model().clear()
    for udi in l:
      if self.get_device_property(udi, "device-is-optical-disc"):
        self.iso_dev_ls.append_text(self.get_device_property(udi, "device-file"))
        n+=1;
    if n: self.iso_dev_ls.set_active(0)

  def refresh_target_dev(self, *args):
    n=0
    l=self.__dev.EnumerateDevices(dbus_interface = interface)
    self.target_dev_ls.get_model().clear()
    for udi in l:
      l.sort()
      if self.get_device_property(udi, "device-is-partition"):
        dv=self.__dev_re.sub('',udi)
        if not self.get_device_property(dv, "device-is-removable"): continue
        nm=str(self.get_device_property(udi, "device-presentation-name")) or str(self.get_device_property(udi, "id-label"))
        fn=str(self.get_device_property(udi, "device-file"))
        s=str(self.get_device_property(udi, "device-size"))
        self.target_dev_ls.append_text(u"%s:%s (%s)" % (fn,s,nm))
        n+=1;
    if n: self.target_dev_ls.set_active(0)


  def is_live(self):
    """return if the currently running OS is a live system and the device the holds the iso image"""
    #try: t1='liveimg' in open('/proc/cmdline','rt').read()
    #except: t1=False
    t=os.path.islink('/dev/live')
    if t: d=os.path.realpath('/dev/live')
    else: d=None
    return t,d

# /usr/bin/livecd-iso-to-disk [--format] [--reset-mbr] [--noverify] [--overlay-size-mb <size>] [--home-size-mb <size>] [--unencrypted-home] [--skipcopy] <isopath> <usbstick device>

