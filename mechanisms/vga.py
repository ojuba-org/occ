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
import re
import os
import os.path
from OjubaControlCenter.mechanismClass import mechanismClass
class OccMechanism(mechanismClass):
  grub_kernels_re=re.compile(r'^(\s*kernel\b.*)$',re.M)
  grub_kms_re=re.compile(r'^(\s*kernel\b.*)(\snomodeset\b)(.*?)$',re.M)
  grub_kernel_vga_re=re.compile(r'^(\s*kernel\b.*)(\svga=\S+\b)(.*?)$',re.M)
  grub_conf='/boot/grub/grub.conf'
  xorg_conf='/etc/X11/xorg.conf'
  drivers='|'.join(['intel','i740','ati','radeon','radeonhd','openchrome'])
  xorg_accel=re.compile(r'^\s*Option\s+"AccelMethod"\s+"([^"]*)"\s*$',re.M | re.I)
  xorg_acceldfs_re=re.compile(r'^\s*Option\s+"AccelDFS"\s+"([^"]*)"\s*$',re.M | re.I)
  xorg_dri_re=re.compile(r'^\s*Option\s+"DRI"\s+"([^"]*)"\s*$',re.M | re.I)
  xorg_swc_re=re.compile(r'^\s*Option\s+"SWCursor"\s+"([^"]*)"\s*$',re.M | re.I)
  xorg_device_re=re.compile(r'''(^\s*Section\s*"Device".*?\bDriver\s*"(%s)")''' % drivers,re.M | re.DOTALL | re.I)

  def __init__(self):
    mechanismClass.__init__(self,'vga')
  def checkKMS(self):
    l=open(self.grub_conf,'rt').read()
    k=self.grub_kernels_re.findall(l)
    m=map(lambda i: 'nomodeset' not in i, k)
    if all(m): return '2'
    elif any(m): return '1'
    else: return '0'
  def disableKMS(self):
    l=open(self.grub_conf,'rt').read()
    l=self.grub_kms_re.sub(r'\1\3',l) # remove nomodeset
    l=self.grub_kernels_re.sub(r'\1 nomodeset',l)
    open(self.grub_conf,'wt').write(l)
    return '0'
  def enableKMS(self):
    l=open(self.grub_conf,'rt').read()
    l=self.grub_kms_re.sub(r'\1\3',l) # remove nomodeset
    open(self.grub_conf,'wt').write(l)
    return '0'
  def rm_kernel_vga(self):
    l=open(self.grub_conf,'rt').read()
    l=self.grub_kernel_vga_re.sub(r'\1\3',l) # remove vga=XYZ
    open(self.grub_conf,'wt').write(l)
    return '0'
  def set_kernel_vga(self,n):
    l=open(self.grub_conf,'rt').read()
    l=self.grub_kernel_vga_re.sub(r'\1\3',l) # remove vga=XYZ
    l=self.grub_kernels_re.sub(r'\1 vga='+n,l)
    open(self.grub_conf,'wt').write(l)
    return '0'

  # xorg.cong manipulation
  def createXorgConf(self):
    return str(os.system("su -l -c 'system-config-display --reconfig --noui'"))

  def saveXorgConf(self, xorgconf):
    if os.path.exists('/etc/X11/xorg.conf'):
      i=0; s=''
      while(os.path.exists('/etc/X11/xorg.conf.occBackup'+s)):
        i+=1; s=str(i)
      try:
        open('/etc/X11/xorg.conf.occBackup'+s,'wt').write(
          open('/etc/X11/xorg.conf','rt').read()
        )
      except IOError: return '-1'
    try: open('/etc/X11/xorg.conf','wt').write(xorgconf)
    except IOError: return '-2'
    return '0'

  def unsetAccel(self):
    if not os.path.exists(self.xorg_conf): return '0'
    l=open(self.xorg_conf,'rt').read()
    l=self.xorg_accel.sub('',l)
    open(self.xorg_conf,'wt').write(l)
    return '0'

  def addXorgOption(self,o,v):
    if not os.path.exists(self.xorg_conf): self.createXorgConf()
    l=open(self.xorg_conf,'rt').read()
    l=re.sub(r'^\s*Option\s+"%s"\s+"([^"]*)"\s*$' % o,'',l)
    l=self.xorg_device_re.sub(r'\1\n  Option "%s" "$s"\n' % (o,v),l)
    open(self.xorg_conf,'wt').write(l)
    return '0'

  def setAccelEXA(self):
    if not os.path.exists(self.xorg_conf): self.createXorgConf()
    l=open(self.xorg_conf,'rt').read()
    l=self.xorg_accel.sub('',l)
    l=self.xorg_device_re.sub(r'\1\n  Option "AccelMethod" "EXA"\n',l)
    open(self.xorg_conf,'wt').write(l)
    return '0'

  def setAccelXAA(self):
    if not os.path.exists(self.xorg_conf): self.createXorgConf()
    l=open(self.xorg_conf,'rt').read()
    l=self.xorg_accel.sub('',l)
    l=self.xorg_device_re.sub(r'\1\n  Option "AccelMethod" "XAA"\n',l)
    open(self.xorg_conf,'wt').write(l)
    return '0'

  def unsetAccelDFS(self):
    if not os.path.exists(self.xorg_conf): return '0'
    l=open(self.xorg_conf,'rt').read()
    l=self.xorg_acceldfs_re.sub('',l)
    open(self.xorg_conf,'wt').write(l)
    return '0'

  def setAccelDFS_off(self):
    if not os.path.exists(self.xorg_conf): self.createXorgConf()
    l=open(self.xorg_conf,'rt').read()
    l=self.xorg_acceldfs_re.sub('',l)
    l=self.xorg_device_re.sub(r'\1\n  Option "AccelDFS" "off"\n',l)
    open(self.xorg_conf,'wt').write(l)
    return '0'

  def unsetDRI(self):
    if not os.path.exists(self.xorg_conf): self.createXorgConf()
    l=open(self.xorg_conf,'rt').read()
    l=self.xorg_dri_re.sub('',l)
    open(self.xorg_conf,'wt').write(l)
    return '0'

  def setDRI_off(self):
    if not os.path.exists(self.xorg_conf): self.createXorgConf()
    l=open(self.xorg_conf,'rt').read()
    l=self.xorg_dri_re.sub('',l)
    l=self.xorg_device_re.sub(r'\1\n  Option "DRI" "off"\n',l)
    open(self.xorg_conf,'wt').write(l)
    return '0'

  def unsetSWC(self):
    if not os.path.exists(self.xorg_conf): self.createXorgConf()
    l=open(self.xorg_conf,'rt').read()
    l=self.xorg_swc_re.sub('',l)
    open(self.xorg_conf,'wt').write(l)
    return '0'

  def setSWC_on(self):
    if not os.path.exists(self.xorg_conf): self.createXorgConf()
    l=open(self.xorg_conf,'rt').read()
    l=self.xorg_swc_re.sub('',l)
    l=self.xorg_device_re.sub(r'\1\n  Option "SWCursor" "on"\n',l)
    open(self.xorg_conf,'wt').write(l)
    return '0'

