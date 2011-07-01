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
import os
import os.path
from OjubaControlCenter.mechanismClass import mechanismClass
class OccMechanism(mechanismClass):
  rule_f='/etc/udev/rules.d/91-occ-usbsw.rules'
  usbsw_path='/usr/bin/usb_modeswitch'
  def __init__(self):
    mechanismClass.__init__(self,'usbsw')

  def sw_now(self,*args):
    if not os.path.exists(self.usbsw_path): return '-1'
    return str(os.system('%s %s' % (self.usbsw_path,' '.join(args))))

  def add_rule(self,c,v,p,*args):
    if not os.path.exists(self.usbsw_path): return '-1'
    a=' '.join(args).replace('"','')
    cmd=('%s %s' % (self.usbsw_path, a))
    l='''\n# %s\nSUBSYSTEM=="usb", SYSFS{idProduct}=="%s", SYSFS{idVendor}=="%s", RUN+="%s"\n''' % (c,p,v,cmd)
    open(self.rule_f,'at+').write(l)
    return '0'

  def remove_all_rules(self):
    if not os.path.exists(self.rule_f): return '-1'
    try: os.unlink(self.rule_f)
    except: return '-1'
    return '0'

