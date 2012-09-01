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

import re
import os
import os.path
from gi.repository import Gtk
from subprocess import *

from OjubaControlCenter.pluginsClass import PluginsClass
from OjubaControlCenter.widgets import error, info, sure

class occPlugin(PluginsClass):
    comment_start=re.compile('^###+$')
    ven_re=re.compile('^\s*;?\s*DefaultVendor\s*=\s*0x([0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f])',re.M)
    pro_re=re.compile('^\s*;?\s*DefaultProduct\s*=\s*0x([0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f])',re.M)
    p_re=re.compile('^\s*;?\s*(\S+)\s*=\s*(\S+)\s*$',re.M)
    args_h={
        'DefaultVendor':'v','DefaultProduct':'p',
        'TargetVendor':'V','TargetProduct':'P','TargetClass':'C',
        'MessageEndpoint':'m','MessageContent':'M',
        'ResponseEndpoint':'r', 'NeedResponse':'n',
        'DetachStorageOnly':'d',
        'HuaweiMode':'H',
        'SierraMode':'S',
        'SonyMode':'O',
        'ResetUSB':'R',
        'CheckSuccess':'s',
        'Interface':'i', 'Configuration':'u', 'AltSetting':'a'
    }
    def __init__(self,ccw):
        PluginsClass.__init__(self, ccw,_('USB Mode Switch'),'net',90)
        vb=Gtk.VBox(False,2)
        self.add(vb)
        hb=Gtk.HBox(False,6); vb.pack_start(hb,True,True,2)
        b=Gtk.Button(_('Remove all applied methods'))
        b.connect('clicked',self.remove_applied)
        hb.pack_start(b,False,False,2)

        hb=Gtk.HBox(False,6); vb.pack_start(hb,True,True,2)
        self.k_ls=Gtk.ComboBoxText()
        self.k_ls.connect('changed', self.update_methods)
        hb.pack_start(Gtk.Label(_('Device ID:')),False,False,2)
        hb.pack_start(self.k_ls,False,False,2)
        b=Gtk.Button(stock=Gtk.STOCK_REFRESH)
        b.connect('clicked',self.refresh)
        hb.pack_start(b,False,False,2)
        self.parse_conf()
            
        hb=Gtk.HBox(False,6); vb.pack_start(hb,True,True,2)
        self.m_ls=Gtk.ComboBoxText()
        self.m_ls.connect('changed', self.update_desc)
        hb.pack_start(Gtk.Label(_('Switch method:')),False,False,2)
        hb.pack_start(self.m_ls,False,False,2)
        
        b=Gtk.Button(_("apply now"))
        b.connect('clicked',self.apply_now)
        hb.pack_start(b,False,False,2)
        b=Gtk.Button(_("always apply this method automatically"))
        b.connect('clicked',self.always_apply)
        hb.pack_start(b,False,False,2)
        hb=Gtk.HBox(False,6); vb.pack_start(hb,True,True,2)
        self.desc=Gtk.Label("%s: %s" % (_('Method details'),_('N/A')))
        hb.pack_start(self.desc,False,False,2)
        self.refresh()

    def __usb_ls(self):
        r=[]
        p1 = Popen(["lsusb"], stdout=PIPE)
        lsusb=p1.communicate()[0].split('\n')
        for l in lsusb:
            a=l.split(' ')
            if len(a)>5: r.append(a[5].lower())
        return r

    def refresh(self, *args):
        self.k_ls.get_model().clear()
        #l=self.usbsw_info.keys() # for testing
        l=filter(lambda i: i in self.usbsw_info.keys(),self.__usb_ls())
        for k in l: self.k_ls.append_text(k)

    def update_desc(self, *args):
        k=self.k_ls.get_active_text()
        i=self.m_ls.get_active()
        if not self.usbsw_info.has_key(k): return
        self.desc.set_text("%s:\n%s" % (_('Method details'),self.usbsw_info[k][i][2]))

    def update_methods(self, *args):
        self.m_ls.get_model().clear()
        k=self.k_ls.get_active_text()
        if not self.usbsw_info.has_key(k): return
        for l in self.usbsw_info[k]: self.m_ls.append_text(l[0])
        self.m_ls.set_active(0)

    def apply_now(self,*args):
        k=self.k_ls.get_active_text()
        i=self.m_ls.get_active()
        if not k or i<0: error(_("no method selected.")); return
        if not self.usbsw_info.has_key(k): error(_("Could not find suitable method.")); return
        r=self.ccw.mechanism('usbsw','sw_now',self.usbsw_info[k][m][1])
        if r!='0': error(_("unexpected return code [%s]." % r))
        else: info(_("Applied successfully"))

    def always_apply(self,*args):
        k=self.k_ls.get_active_text()
        i=self.m_ls.get_active()
        if not k or i<0: error(_("no method selected.")); return
        if not sure(_('Are you sure you want to apply this method automatically. You may want to try the "apply now" button first.')): return
        if not self.usbsw_info.has_key(k): error(_("Could not find suitable method.")); return
        r=self.ccw.mechanism('usbsw','add_rule',self.usbsw_info[k][m][1])
        if r!='0': error(_("unexpected return code [%s]." % r))
        else: info(_("Applied successfully"))

    def remove_applied(self,*args):
        if not sure(_('Are you sure you want to remove all permanently applied methods.')): return
        r=self.ccw.mechanism('usbsw','remove_all_rules')
        if r!='0': error(_("unexpected return code [%s]." % r))
        else: info(_("Applied successfully"))

    def to_args(self,b):
        t=b.split('\n')[1][2:]
        r=[]
        a=""
        h={}
        for k,v in self.p_re.findall(b):
            v=v.replace(';','')
            if self.args_h.has_key(k) and k!='HuaweiMode' and k!='Configuration': a+=' -%s %s' % (self.args_h[k],v)
            h[self.args_h[k]]=v
        # special cases
        if h.has_key('O') and h.has_key('u'):
            r.append((t,a,b))
            del h['O']
            a=" ".join(map(lambda k: '-%s %s' % (k,h[k]),h.keys()))
            r.append((t+" #2",a,b))
        if h.has_key('d') and h.has_key('H'): 
            r.append((t,a,b))
            del h['d']
            a=" ".join(map(lambda k: '-%s %s' % (k,h[k]),h.keys()))
            r.append((t+" #2",a,b))
        else:
            r.append((t,a,b))
        return r

    def parse_conf(self):
        block_start=0
        b=''
        blocks=[]
        p={}
        for l in open('/etc/usb_modeswitch.conf','rt'):
            if self.comment_start.match(l):
                if b: blocks.append(b)
                block_start=1; b=""
            if block_start==1: b+=l
        if b: blocks.append(b)
        for b in blocks:
            s=self.ven_re.findall(b)[0].lower()+':'+self.pro_re.findall(b)[0].lower()
            if p.has_key(s): p[s].extend(self.to_args(b))
            else: p[s]=self.to_args(b)
        self.usbsw_info=p

