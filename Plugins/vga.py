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
import pty
import signal
import os
import re
import time
import gtk

from subprocess import Popen, PIPE

from OjubaControlCenter.pluginsClass import PluginsClass
from OjubaControlCenter.widgets import run_in_bg
from OjubaControlCenter.widgets import LaunchOrInstall, info, error

class occPlugin(PluginsClass):
  gears_re=re.compile("^\s*(\d+)(\.\d+)? frames in (\d+)(\.\d+)? seconds = (\d+)(\.\d+)? FPS\s*$")
  via='1106'
  intel='8086'
  ati='1002'
  nvidia='10de'
  nvidia_185_pciid=['0040', '0041', '0042', '0043', '0044', '0045', '0046', '0047', '0048', '0090', '0091', '0092', '0093', '0095', '0098', '0099', '00c0', '00c1', '00c2', '00c3', '00c8', '00c9', '00f1', '00f2', '00f3', '00f4', '00f5', '00f6', '00f9', '0140', '0141', '0142', '0143', '0144', '0145', '0146', '0147', '0148', '0149', '014f', '0160', '0161', '0162', '0163', '0164', '0166', '0167', '0168', '0169', '016a', '0191', '0193', '0194', '0197', '01d0', '01d1', '01d3', '01d6', '01d7', '01d8', '01dd', '01df', '0221', '0222', '0240', '0241', '0242', '0244', '0247', '0290', '0291', '0292', '0293', '0294', '0295', '0297', '0298', '0299', '02e0', '02e1', '02e2', '02e3', '02e4', '0390', '0391', '0392', '0393', '0394', '0395', '0397', '0398', '0399', '03d0', '03d1', '03d2', '03d5', '0400', '0401', '0402', '0403', '0404', '0405', '0407', '0408', '0409', '0420', '0421', '0422', '0423', '0424', '0425', '0426', '0427', '0428', '042c', '042e', '0531', '0533', '053a', '053b', '053e', '05e0', '05e1', '05e2', '05e3', '0600', '0601', '0602', '0604', '0605', '0606', '0608', '0609', '060b', '060c', '060d', '0610', '0611', '0612', '0613', '0614', '0615', '0617', '0622', '0623', '0625', '0626', '0627', '0628', '062a', '062b', '062c', '0640', '0641', '0643', '0646', '0647', '0648', '0649', '064a', '064b', '064c', '0656', '06e0', '06e1', '06e4', '06e5', '06e6', '06e8', '06e9', '07e0', '07e1', '07e3', '0844', '0845', '0847', '0848', '0849', '084a', '084b', '084c', '084d', '084f', '0862', '0863', '086c', '004e', '009d', '00cc', '00cd', '00ce', '00f8', '014a', '014c', '014d', '014e', '0165', '019d', '019e', '01d7', '01da', '01db', '01dc', '01de', '0245', '029a', '029b', '029c', '029d', '029e', '029f', '039e', '040a', '040b', '040c', '040d', '040e', '040f', '0429', '042a', '042b', '042d', '042f', '05f9', '05fd', '05fe', '05ff', '061a', '061c', '061e', '0638', '063a', '0658', '0659', '065c', '06ea', '06eb', '06f8', '06f9', '06fa', '06fd', '087a', '087f']
  nvidia_173_pciid=['00fa', '00fb', '00fc', '00fd', '00fe', '0301', '0302', '0308', '0309', '0311', '0312', '0314', '031a', '031b', '031c', '0320', '0321', '0322', '0323', '0324', '0325', '0326', '0327', '0328', '032a', '032b', '032c', '032d', '0330', '0331', '0332', '0333', '0334', '0338', '033f', '0341', '0342', '0343', '0344', '0347', '0348', '034c', '034e']
  nvidia_96_pciid=['0110', '0111', '0112', '0113', '0170', '0171', '0172', '0173', '0174', '0175', '0176', '0177', '0178', '0179', '017a', '017c', '017d', '0181', '0182', '0183', '0185', '0188', '018a', '018b', '018c', '01a0', '01f0', '0200', '0201', '0202', '0203', '0250', '0251', '0253', '0258', '0259', '025b', '0280', '0281', '0282', '0286', '0288', '0289', '028c']
  nvidia_71_pciid=['0020', '0028', '0029', '002c', '002d', '00a0', '0100', '0101', '0103', '0150', '0151', '0152', '0153']
  nvidia_kmod={185:'kmod-nvidia',173:'kmod-nvidia-173xx',96:'kmod-nvidia-96xx',71:'kmod-nvidia-96xx'}
  nvidia_dict=None
  def __init__(self,ccw):
    self.__lspci=None
    PluginsClass.__init__(self, ccw,_('Display settings and tools'),'hw',10)
    self.__dri=None
    self.fps=None
    vb=gtk.VBox(False,2)
    self.add(vb)
    hb=gtk.HBox(False,2)
    vb.pack_start(hb,True,True,2)
    l=gtk.Label()
    l.set_markup(self.dri_result())
    hb.pack_start(l,False,False,2)
    hb=gtk.HBox(False,2)
    vb.pack_start(hb,False,False,2)
    hb.pack_start(gtk.Label(_("glxgears Result:")),False,False,2)
    self.l=gtk.Label(_("N/A"))
    hb.pack_start(self.l,False,False,2)
    self.gears_b=gtk.Button(stock=gtk.STOCK_EXECUTE)
    hb.pack_start(self.gears_b,False,False,2)
    hb.pack_start(gtk.VBox(),True,True,2)
    hb=gtk.HBox(False,2)
    vb.pack_start(hb,True,True,2)
    self.suggestion=gtk.Label()
    hb.pack_start(self.suggestion,False,False,2)
    self.gears_b.connect('clicked',self.gearsExecute)
    self.advanced=gtk.Expander(_("Advanced options"))
    vb.pack_start(self.advanced,True,True,2)
    vb=gtk.VBox(False,2)
    self.advanced.add(vb)
    self.__nvidia_gui_init(vb)
    hb=gtk.HBox(False,6); vb.pack_start(hb,True,True,2)
    self.checkKMS_b=gtk.Button(_("check KMS"))
    self.disableKMS_b=gtk.Button(_("disable KMS"))
    self.enableKMS_b=gtk.Button(_("enable KMS"))
    hb.pack_start(self.checkKMS_b,False,False,2)
    hb.pack_start(self.disableKMS_b,False,False,2)
    hb.pack_start(self.enableKMS_b,False,False,2)
    self.checkKMS_b.connect('clicked',self.checkKMS)
    self.disableKMS_b.connect('clicked',self.disableKMS)
    self.enableKMS_b.connect('clicked',self.enableKMS)
    hb=gtk.HBox(False,6); vb.pack_start(hb,True,True,2)
    hb.pack_start(LaunchOrInstall(self, _('Configure Display'),'/usr/bin/system-config-display',['system-config-display']),False,False,0)
    #self.xorgConf=gtk.Button(_("create xorg.conf"))
    #hb.pack_start(self.xorgConf,False,False,0)
    #self.xorgConf.connect('clicked',self.call_vga_mechanism,'createXorgConf')
    self.__ati_gui_init(vb)
    hb=gtk.HBox(False,6); vb.pack_start(hb,True,True,2)
    self.accelEXA=gtk.Button(_("use EXA acceleration"))
    self.accelEXA.connect('clicked', self.call_vga_mechanism,'setAccelEXA')
    hb.pack_start(self.accelEXA,False,False,0)
    self.accelXAA=gtk.Button(_("use XAA acceleration"))
    self.accelXAA.connect('clicked', self.call_vga_mechanism,'setAccelXAA')
    hb.pack_start(self.accelXAA,False,False,0)
    self.accelDef=gtk.Button(_("use default acceleration"))
    self.accelDef.connect('clicked', self.call_vga_mechanism,'unsetAccel')
    hb.pack_start(self.accelDef,False,False,0)
    hb=gtk.HBox(False,6); vb.pack_start(hb,True,True,2)
    self.swCursor=gtk.Button(_("use software cursor"))
    self.swCursor.connect('clicked',self.call_vga_mechanism,'setSWC_on')
    hb.pack_start(self.swCursor,False,False,0)
    self.swCursorDef=gtk.Button(_("use default cursor"))
    self.swCursorDef.connect('clicked', self.call_vga_mechanism, 'unsetSWC')
    hb.pack_start(self.swCursorDef,False,False,0)
    #vb.pack_start(gtk.Label("fooo:"),False,False,2)
    self.suggest()

  def __ati_gui_init(self,vb):
    l=map(lambda i: i[0],self.__vga_pciid())
    if self.ati not in l: return
    hb=gtk.HBox(False,6); vb.pack_start(hb,True,True,2)
    b=gtk.Button(_("Disable DFS Acceleration"))
    b.connect('clicked', self.call_vga_mechanism, 'setAccelDFS_off')
    hb.pack_start(b,False,False,0)
    b=gtk.Button(_("default DFS settings"))
    b.connect('clicked', self.call_vga_mechanism, 'unsetAccelDFS')
    hb.pack_start(b,False,False,0)

  def call_vga_mechanism(self,b,m):
    s=self.ccw.mechanism('vga',m)
    if s == 'NotAuth': return
    if s=='0': info(_('Done.'),self.ccw)
    else: error(_('unexpected return code, possible an error had occurred.'),self.ccw)

  def __nvidia_gui_init(self,vb):
    nv=self.is_nvidia()
    if not nv: return
    hb=gtk.HBox(False,6); vb.pack_start(hb,True,True,2)
    b=gtk.Label(_("Install proprietary nVidia drivers:"))
    hb.pack_start(b,False,False,2)
    self.kmod_nvidia_ls=gtk.combo_box_new_text()
    if nv==-1: 
      for k in [185,173,96]: self.kmod_nvidia_ls.append_text(self.nvidia_kmod[k])
    else:
      self.kmod_nvidia_ls.append_text(self.nvidia_kmod[nv])
    self.kmod_nvidia_ls.set_active(0)
    hb.pack_start(self.kmod_nvidia_ls,False,False,2)
    b=gtk.Button(stock=gtk.STOCK_APPLY)
    b.connect('clicked',self.install_nvidia)
    hb.pack_start(b,False,False,2)
    hb=gtk.HBox(False,6); vb.pack_start(hb,True,True,2)
    hb.pack_start(LaunchOrInstall(self.ccw, _("Enable proprietary drivers"),'/usr/bin/livna-config-display', ['livna-config-display']),False,False,2)
    b=gtk.Button(_("nVidia Settings"))
    b.connect('clicked',self.__nvidia_settings_cb)
    hb.pack_start(b,False,False,2)

  def install_nvidia(self, b):
    kmod=self.kmod_nvidia_ls.get_active_text()
    if os.uname()[2].endswith('PAE'): kmod+='-PAE'
    print kmod
    print self.ccw.is_installed([kmod])
    if self.ccw.is_installed([kmod]):
      info(_('proprietary nVidia drivers [%s] already installed.') % kmod,self.ccw)
    else: self.ccw.install_packages([kmod])

  def __nvidia_settings_cb(self,b):
    #self.ccw.mechanism('run','in_bg','/usr/bin/nvidia-settings')
    run_in_bg('/usr/bin/nvidia-settings')

  def __lspci_n(self):
    if self.__lspci: return self.__lspci
    p1 = Popen(["lspci","-n"], stdout=PIPE)
    self.__lspci=filter(lambda j: len(j)>=3, map(lambda i: i.split(' ',3),p1.communicate()[0].lower().splitlines()))
    return self.__lspci
  def __vga_pciid(self):
    return map(lambda i: i[2].split(':'),filter(lambda j: j[1]=='0300:', self.__lspci_n()))
  def __suggest_disable_KMS(self):
    l=map(lambda i: i[0],self.__vga_pciid())
    if self.intel in l or self.ati in l: return True
    return False

  def is_nvidia(self):
    l=filter(lambda i: i[0]==self.nvidia,self.__vga_pciid())
    if not l: return 0
    if not self.nvidia_dict:
      self.nvidia_dict=[]
      self.nvidia_dict+=[(i,185) for i in self.nvidia_185_pciid]
      self.nvidia_dict+=[(i,173) for i in self.nvidia_173_pciid]
      self.nvidia_dict+=[(i,96) for i in self.nvidia_96_pciid]
      self.nvidia_dict+=[(i,71) for i in self.nvidia_71_pciid]
      self.nvidia_dict=dict(self.nvidia_dict)
    m=max(map(lambda i: self.nvidia_dict.get(i[1],0), l))
    if m: return m
    return -1 # true but unknown
  def __lsmod_nvidia(self):
    env=os.environ.copy()
    env['LC_ALL']='C'
    lsmod=Popen(["lsmod"], stdout=PIPE, env=env).communicate()[0]
    return 'nvidia' in lsmod

  def checkKMS(self,*args):
    s=self.ccw.mechanism('vga','checkKMS')
    if s == 'NotAuth': return
    if s=='2': info(_('KMS is enabled for all kernels.\nNote: You may need to remake grub config file.'),self.ccw)
    elif s=='1': info(_('KMS is enabled for some kernels, and disabled for others.'),self.ccw)
    elif s=='0': info(_('KMS is disabled for all kernels.\nNote: You may need to remake grub config file.'),self.ccw)
    else: error(_('unexpected return code, possible an error had occurred.'),self.ccw)
  def disableKMS(self,*args):
    s=self.ccw.mechanism('vga','disableKMS')
    if s == 'NotAuth': return
    if s=='0': info(_('KMS is now disabled for all kernels.'),self.ccw)
    else: error(_('unexpected return code, possible an error had occurred.'%s),self.ccw)
  def enableKMS(self,*args):
    s=self.ccw.mechanism('vga','enableKMS')
    if s == 'NotAuth': return
    if s=='0': info(_('KMS is now enabled for all kernels.'),self.ccw)
    else: error(_('unexpected return code, possible an error had occurred.'),self.ccw)
    
  def isdri(self):
    if self.__dri!=None: return self.__dri
    env=os.environ.copy(); env['LC_ALL']='C'
    glxinfo = Popen(["glxinfo"], stdout=PIPE, env=env).communicate()[0].split('\n')
    for l in glxinfo:
      l=l.strip()
      if l.startswith("direct rendering: "): 
        if l[18:]=="Yes": self.__dri=True; return True
        else: self.__dri=False; return False
    self.__dri=False
    return False
  def dri_result(self):
    if self.isdri():
      s=_("""Your VGA driver supports direct rendering.
Before you enable special effects please perform 5 second glxgears speed test.""")
    else:
      s=_("""Your VGA driver does <span color='red'><b>not</b></span> support direct rendering.
You should <b>not</b> enable special effects till you solve this problem.
You may want to check how slow is your VGA card by performing 5 second glxgears speed test.""")
    return s

  def suggest(self):
    s2=""
    e=False
    if not self.fps:
      s=_("""If you got more than <b>500 FPS</b> then you may use special effects efficiently.""")
    elif self.fps>=500 and self.isdri():
      s=_("""Your VGA card performance is good. you may enjoy special effects.""")
    elif self.isdri():
      s=_("""Although your VGA card driver supports direct rendering, it has poor performance.""")
      s2=_("we don't recommend enabling special effects until you fix this issue by one or more of the advanced options below.")
      e=True
    else:
      s=_("""You might enhance your VGA performance by trying one or more of the advanced options below.""")
      e=True
    if self.is_nvidia() and not self.__lsmod_nvidia():
      s2=_("nVidia Proprietary drivers are not loaded. You may enhance graphics performance by installing nvidia proprietary drivers.")
      e=True
    if self.__suggest_disable_KMS():
      s2=_("Some cards have problems with KMS, try to disable KMS and reboot.")
      e=True
    if s2: s=u"\n".join((s,s2,))
    self.suggestion.set_markup(s)
    self.advanced.set_expanded(e)
    
  def gearsExecute(self,*args):
    self.l.set_text(_("wait 5 seconds"))
    while (gtk.events_pending ()): gtk.main_iteration ()
    env=os.environ.copy()
    env['LC_ALL']='C'
    pid,fd=pty.fork()
    if pid==0: os.execvpe('glxgears',['glxgears',],env=env)
    f=os.fdopen(fd)
    n=0
    m=None
    while(not m and n<10):
      try: l=f.readline()
      except IOError: break
      m=self.gears_re.match(l)
      n+=1
    os.kill(pid,signal.SIGTERM)
    if not m: self.fps=None
    else:
      try: self.fps=int(m.group(5))
      except ValueError: self.fps=None
    self.l.set_text("%s" % (str(self.fps)+_(" FPS"),_('N/A'))[self.fps==None])
    self.suggest()
    
# TODO: check driver if it's nvidia, intel, i740, radeon, radeonhd
# add '''Option "AccelMethod" "EXA"''' or XAA (traditional mode) or remove "AccelMethod" to use the default "UXA" (intel KMS) "EXA" (intel no KMS)
# check the man of each driver
# in case of ati/amd Option "AccelDFS" "off" might help
# and for openchrome
# Option "SWCursor"  "boolean"

