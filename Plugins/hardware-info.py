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

from gi.repository import Gtk
import re
from subprocess import Popen, PIPE
from OjubaControlCenter.pluginsClass import PluginsClass
from OjubaControlCenter.widgets import LaunchOrInstall, error, info

## NOTE: these global vars is loader validators
category = 'hw'
caption = _('Hardware Information')
description = ''
priority = 0

class occPlugin(PluginsClass):
  cpu_re=re.compile(r"^\s*model name\s*:\s*(.*)\s*$",re.M)
  cache_re=re.compile(r"^\s*cache size\s*:\s*(.*)\s*$",re.M)
  mem_re=re.compile(r"^\s*MemTotal\s*:\s*(.*)\s*$",re.M)
  swap_re=re.compile(r"^\s*SwapTotal\s*:\s*(.*)\s*$",re.M)
  def __init__(self,ccw):
    PluginsClass.__init__(self, ccw, caption, category, priority)
    vb=Gtk.VBox(False,2)
    self.add(vb)
    h=Gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    self.l=Gtk.Label()
    h.pack_start(self.l,False,False,0)
    hb=Gtk.HBox(False,2)
    vb.pack_start(hb,False,False,0)
    #hb.pack_start(Gtk.VBox(False,0),True,True,6)
    self.r=Gtk.Button(stock=Gtk.STOCK_REFRESH)
    self.r.connect('clicked',self.__update)
    hb.pack_start(self.r,False,False,6)
    hb.pack_start(LaunchOrInstall(self,_('Details'),'/usr/bin/hardinfo',['hardinfo']),False,False,0)
    b=Gtk.Button(_('Update PCI ID database'))
    b.connect('clicked', self.__update_pciid_cb)
    hb.pack_start(b,False,False,0)
    self.__update()

  def __update_pciid_cb(self, b):
    r=self.ccw.mechanism('run','system','update-pciids -q')
    if r == 'NotAuth': return
    if r!='0': error(_("unexpected return code, possible an error had occurred."), self.ccw)
    else: info(_('Done.'), self.ccw)

  def __cpu_and_mem(self):
    l=open('/proc/cpuinfo','rt').read()
    self.cpu=self.cpu_re.findall(l)[0]
    self.cache=self.cache_re.findall(l)[0]
    l=open('/proc/meminfo','rt').read()
    self.mem=self.mem_re.findall(l)[0]
    self.swap=self.swap_re.findall(l)[0]
  def __lspci(self,*args):
    p1 = Popen(["lspci"], stdout=PIPE)
    return p1.communicate()[0]
  def __refresh_usb(self,*args):
    p1 = Popen(["lsusb"], stdout=PIPE)
    self.lsusb='\n'.join(filter(lambda i: ' root hub' not in i,p1.communicate()[0].split('\n')))
  def __refresh_pci(self):
    self.lspci=self.__lspci().split('\n')
    self.vga=filter(lambda i: 'VGA' in i, self.lspci)
    self.sound=filter(lambda i: 'Audio' in i or 'audio' in i,self.lspci)
  def __update(self,*args):
    self.__cpu_and_mem()
    self.__refresh_pci()
    self.__refresh_usb()
    self.l.set_markup('''\
<span size="large" weight="bold">%s:</span>\n%s cache=%s
<span size="large" weight="bold">%s:</span>\nmem=%s swap=%s
<span size="large" weight="bold">%s:</span>\n%s
<span size="large" weight="bold">%s:</span>\n%s
<span size="large" weight="bold">%s:</span>\n%s''' \
      % (_('CPU'),self.cpu,self.cache,\
      _('Memory'),self.mem,self.swap,\
      _('VGA'),'\n'.join(self.vga),_('Sound card'),'\n'.join(self.sound),_('USB'),self.lsusb))

