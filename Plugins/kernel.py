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
import re, os, rpm
from glob import glob
from OjubaControlCenter.widgets import NiceButton, InstallOrInactive, sure, info, error
from OjubaControlCenter.pluginsClass import PluginsClass

class occPlugin(PluginsClass):
  __rre=re.compile(r"-\d\.")
  def __init__(self,ccw):
    PluginsClass.__init__(self, ccw,_('System Kernel:'),'boot',50)
    vb=gtk.VBox(False,2)
    self.add(vb)
    self.__k_r=os.uname()[2]
    if self.__k_r.endswith('.PAE'): self.__kernel='kernel-PAE'
    else: self.__kernel='kernel'
    
    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    l=gtk.Label(_("Linux kernel is the part of the system that deal with the hardware.\nFor safety the system will keep older kernels,\nso that you can use them if the new kernel went wrong.\nBut usually you don't need to keep them if the newer one works fine."))
    h.pack_start(l, False,False,2)
    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    b=gtk.Button(_("Keep only one kernel"))
    b.set_sensitive(self.__count_kernels()>1)
    b.connect('clicked', self.__one_kernel)
    h.pack_start(b, False,False,2)
    if os.uname()[4]!='x86_64':
      h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
      l=gtk.Label(_('A typical kernel can deal with up to 4GB of RAM.\nPAE kernels can deal with much much more than that.'))
      h.pack_start(l,False,False,2)
      h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
      b=InstallOrInactive(self, _("Install PAE kernel"),_("PAE kernel is installed"), _('kernel which supports larger memory'), ['kernel-PAE'])
      h.pack_start(b, False,False,2)

    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    l=gtk.Label()
    l.set_markup(_("There are two types of drivers: <i>kmods</i> and <i><b>a</b>kmods</i>.\nAlthough <b>akmod</b> drivers requires: more disk space for the development dependencies,\nthey will automatically generate drivers for\nnewly-installed kernels without breaking the dependency.\nWe strongly recommend that you use <b>akmod</b>."))
    h.pack_start(l, False,False,2)
    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    b=gtk.Button(_("Install corresponding akmods for installed kmods"))
    b.connect('clicked',self.__akmods_cb)
    h.pack_start(b,False,False,2)
    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    l=gtk.Label(_("Developers need kernel documentation and kernel development tools"))
    h.pack_start(l, False,False,2)
    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    b=InstallOrInactive(self, _("Install kernel documentation"),_("kernel documentation is already installed"),_('Kernel documentation'),["kernel-doc"])
    h.pack_start(b, False,False,2)
    b=InstallOrInactive(self, _("Install kernel development tools"),_("kernel development package is already installed"),_('needed for building kernel module'),[self.__kernel+"-devel"])
    h.pack_start(b, False,False,2)

  def __get_kmods(self):
    ts = rpm.TransactionSet()
    kmods=[]
    mi = ts.dbMatch()
    mi.pattern('name', rpm.RPMMIRE_GLOB, 'kmod-*')
    for i in mi:
      m=self.__rre.search(i['name'])
      if m: kmods.append(i['name'][:m.start()])
      else: kmods.append(i['name'])
    # uniq
    k={}
    for i in kmods:
      if i.endswith('-PAE'): i=i[:-4]
      k[i]=i
    return k.keys()

  def __get_akmods(self):
    return map(lambda i: "a"+i , self.__get_kmods())
  
  def __count_kernels(self):
    ts = rpm.TransactionSet()
    k1=ts.dbMatch('name','kernel').count()
    k2=ts.dbMatch('name','kernel-PAE').count()
    return k1+k2

  def __one_kernel(self, *args):
    r=self.ccw.mechanism('run','system','package-cleanup -y --oldkernels --count=1')
    if r=='0': info(_("Done."))
    else: error(_("unexpected return code, possible an error had occurred."))

  def __akmods_cb(self, b):
    p=self.__get_akmods()
    if self.ccw.is_installed(p):
      info(_("all needed akmods are already installed."))
    else:
      self.ccw.install_packages(p)

