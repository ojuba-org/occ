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

#import pty
#import signal
#import time
from gi.repository import Gtk
import os
import re
from glob import glob
from subprocess import Popen, PIPE
from OjubaControlCenter.pluginsClass import PluginsClass
from OjubaControlCenter.widgets import LaunchOrInstall, sure, info, error

class occPlugin(PluginsClass):
  amixer_re=re.compile("""^\S[^'\n]+'([^'\n]+)'""",re.M)
  pa_conf='/etc/pulse/default.pa'
  pa_daemon_conf='/etc/pulse/daemon.conf'
  tsched0=re.compile(r"^\s*(load-module module-hal-detect.*?)\btsched\s*=\s*(\S+)\b(.*?)$", re.M)
  rt_re=re.compile('^\s*realtime-scheduling\s*=\s*yes\s*$', re.M)
  def __init__(self,ccw):
    self.__hda_verb_needed=None
    PluginsClass.__init__(self, ccw,_('Sound settings and tools'),'hw',20)
    vb=Gtk.VBox(False,2)
    self.add(vb)
    hb=Gtk.HBox(False,2); vb.pack_start(hb,True,True,2)
    hb.pack_start(Gtk.Label(_("Warning: using headphone at high volume may harm your ears.")),False,False,2)
    hb=Gtk.HBox(False,2); vb.pack_start(hb,True,True,2)
    b=Gtk.Button(_("volume up!"))
    hb.pack_start(b,False,False,2)
    b.connect('clicked',self.vol_up_cb)
    hb.pack_start(LaunchOrInstall(self, _("Simple gnome mixer"), '/usr/bin/gnome-volume-control', ['gnome-media']),False,False,2)
    hb.pack_start(LaunchOrInstall(self, _("Advanced mixer"), '/usr/bin/gst-mixer', ['gst-mixer']),False,False,2)

    e=self.is_hda_verb_needed()
    s=[]
    if e: s.append(_("You may need to use HDA fix from advanced options below."))

    if s:
      hb=Gtk.HBox(False,2); vb.pack_start(hb,True,True,2)
      hb.pack_start(Gtk.Label("\n".join(s)),False,False,2)

    hb.pack_start(Gtk.VBox(False,2),False,False,2)
    self.advanced=Gtk.Expander()
    self.advanced.set_label(_("Advanced options"))
    vb.pack_start(self.advanced,True,True,2)
    vb=Gtk.VBox(False,2)
    self.advanced.add(vb)
    hb=Gtk.HBox(False,6); vb.pack_start(hb,True,True,2)
    hb.pack_start(Gtk.Label(_("HDA fix for Acer Aspire 8920G:")),False,False,2)
    b=Gtk.Button(_("apply now"))
    b.connect('clicked', self.hda_verb_now)
    hb.pack_start(b,False,False,2)
    b=Gtk.Button(_("enable at boot"))
    b.connect('clicked', self.hda_verb_at_boot)
    hb.pack_start(b,False,False,2)
    b=Gtk.Button(_("remove from boot"))
    b.connect('clicked', self.remove_from_boot)
    hb.pack_start(b,False,False,2)
    
    hb=Gtk.HBox(False,6); vb.pack_start(hb,True,True,2)
    hb.pack_start(Gtk.Label(_("By default sound works in time-based scheduling which consumes less power and CPU load.\nBut some drivers have a problem with time mode.\nIf you experience skipping in sound you may disable this feature.")),False,False,2)
    hb=Gtk.HBox(False,6); vb.pack_start(hb,True,True,2)
    self.tbs=Gtk.CheckButton(_("Time-based scheduling"))
    hb.pack_start(self.tbs,False,False,2)
    b=Gtk.Button(stock=Gtk.STOCK_APPLY)
    b.connect('clicked', self.tbs_cb)
    hb.pack_start(b,False,False,2)
    hb=Gtk.HBox(False,6); vb.pack_start(hb,True,True,2)
    hb.pack_start(Gtk.Label(_("If you have disabled time-based scheduling and the sound still skips, try setting realtime scheduling.")),False,False,2)
    hb=Gtk.HBox(False,6); vb.pack_start(hb,True,True,2)
    self.rt_b=Gtk.CheckButton(_("Realtime scheduling"))
    hb.pack_start(self.rt_b,False,False,2)
    b=Gtk.Button(stock=Gtk.STOCK_APPLY)
    b.connect('clicked', self.rt_cb)
    hb.pack_start(b,False,False,2)
    self.set_checkbox()
    self.advanced.set_expanded(e)

  def set_checkbox(self):
    self.tbs.set_active(self.is_tsched())
    self.rt_b.set_active(self.is_rt())

  def vol_up_cb(self,*args):
    env=os.environ; env['LC_ALL']='C'
    cards=map(lambda i: int(i[17]),glob('/proc/asound/card[0-9]'))
    for i in cards:
      o=Popen(['amixer', '-c',str(i)], stdout=PIPE, env=env).communicate()[0]
      for c in self.amixer_re.findall(o):
        os.system('amixer -c %d set "%s" 100%%' % (i,c))

  def hda_verb_sure(self):
    if self.is_hda_verb_needed(): msg="It seems that your sound card does not need this fix\nAre you still sure you want to run it?"
    else: msg="Are you sure you want to send HDA fix command?"
    return sure(msg, self.ccw)

  def hda_verb_now(self,*args):
    if not self.sure(): return
    r=self.ccw.mechanism('snd','hda_verb','/dev/snd/hwC0D0 0x15 SET_EAPD_BTLENABLE 2')
    if r == 'NotAuth': return
    #os.system("hda-verb /dev/snd/hwC0D0 0x15 SET_EAPD_BTLENABLE 2")
    info(_('Done.'), self.ccw)

  def hda_verb_at_boot(self,*args):
    if not self.sure(): return
    r=self.ccw.mechanism('snd','add_hda_verb','/dev/snd/hwC0D0 0x15 SET_EAPD_BTLENABLE 2')
    if r == 'NotAuth': return
    info(_('Done. New settings will take effect on next boot.'), self.ccw)

  def remove_from_boot(self,*args):
    if not sure(_("Are you sure you want to disable an already enabled hda fix ?"), self.ccw): return
    r=self.ccw.mechanism('snd','remove_hda_verb')
    if r == 'NotAuth': return
    info(_('Done. New settings will take effect on next boot.'), self.ccw)

  def is_hda_verb_needed(self):
    if self.__hda_verb_needed!=None: return self.__hda_verb_needed
    self.__hda_verb_needed=False
    codecs=[]
    chipsets=[]
    lspci = Popen(["lspci"], stdout=PIPE).communicate()[0].split('\n')
    for i in lspci:
      l=i.split(':',1)
      if l[0].endswith('Audio device'): chipsets.append(l[1].strip())
    for fn in glob('/proc/asound/card0/codec#*'):
      for l in open(fn,'rt'):
        if l.startswith('Codec:'): codecs.append(l.split(':',1)[-1].strip())
    if 'Realtek ALC889' in codecs or 'Intel Corporation 82801I (ICH9 Family) HD Audio Controller (rev 03)' in chipsets: self.__hda_verb_needed=True
    return self.__hda_verb_needed

  def tbs_cb(self,b):
    if self.tbs.get_active(): r=self.ccw.mechanism('snd','enable_tsched')
    else: r=self.ccw.mechanism('snd','disable_tsched')
    if r == 'NotAuth': return
    self.set_checkbox()
    info(_('Done. New settings will take effect on next boot.'), self.ccw)

  def rt_cb(self,b):
    if self.rt_b.get_active(): r=self.ccw.mechanism('snd','enable_rt')
    else: r=self.ccw.mechanism('snd','reset_rt')
    if r == 'NotAuth': return
    self.set_checkbox()
    info(_('Done. New settings will take effect on next boot.'), self.ccw)

  def is_tsched(self):
    t=open(self.pa_conf,'rt').read()
    m=self.tsched0.search(t)
    if not m: return True
    s=m.group(2).lower()
    return s=='1' or s=='yes' or s=='true'

  def is_rt(self):
    t=open(self.pa_daemon_conf,'rt').read()
    if self.rt_re.search(t): return True
    return False

