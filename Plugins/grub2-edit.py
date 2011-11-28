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
import gtk
import os
from OjubaControlCenter.utils import cmd_out
from OjubaControlCenter.widgets import InstallOrInactive, sure, info, error, wait
from OjubaControlCenter.pluginsClass import PluginsClass

class occPlugin(PluginsClass):
  conf={}
  conf_fn='/etc/default/grub'
  font_fn='/usr/share/fonts/dejavu/DejaVuSansMono.ttf'
  font_nm='Sans'
  bg_fn='/usr/share/backgrounds/verne/default/normalish/verne.png'
  gfxmode='800x600'
  def __init__(self,ccw):
    PluginsClass.__init__(self, ccw,_('Grub2 settings:'),'boot',30)
    self.load_conf()
    vb=gtk.VBox(False,2)
    self.add(vb)

    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    l=gtk.Label(_("This section will help you to change grub2 settings"))
    h.pack_start(l, False,False,2)
    
    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    h.pack_start(gtk.Label('%s :' % _("Time out")), False,False,2)
    self.Time_Out = b = gtk.SpinButton(gtk.Adjustment(1, 1, 90, 1, 1))
    h.pack_start(b, False,False,2)
    h.pack_start(gtk.Label(_("Seconds")), False,False,2)
    
    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    h.pack_start(gtk.Label('%s :' % _("Kernel options")), False,False,2)
    self.Kernel_Opt = e = gtk.Entry()
    e.set_width_chars(50)
    h.pack_start(e, False,False,2)
    
    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    self.recovery_c = c = gtk.CheckButton(_('Enabel recovery option'))
    h.pack_start(c, False,False,2)
    
    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    self.theme_c = c = gtk.CheckButton(_('Enabel Grub2 theme'))
    c.connect('toggled',self.update_theme_cb)
    h.pack_start(c, False,False,2)
    
    if os.path.isfile(self.conf['FONT_FILE']): self.font_fn=self.conf['FONT_FILE']
    self.font_nm = self.conf['FONT_NAME'] = self.conf['FONT_NAME'].replace('_',' ')
    self.gfxmode = self.conf['GRUB_GFXMODE']
    
    # Grub2 theme frame
    self.tf = f = gtk.Frame(_('Grub2 Theme:')); vb.pack_start(f,False,False,6)
    vbox = gtk.VBox(False,2)
    f.add(vbox)
    
    h=gtk.HBox(False,2); vbox.pack_start(h,False,False,6)
    l=gtk.Label(_("This section will help you to change grub2 Font and background (theme)."))
    h.pack_start(l, False,False,2)
    
    h=gtk.HBox(False,2); vbox.pack_start(h,False,False,6)
    # TODO: customizable BACKGROUND
    l=gtk.Label("%s = '%s'" %(_("We Will Set BACKGROUND"),self.bg_fn))
    h.pack_start(l, False,False,2)
    
    h=gtk.HBox(False,2); vbox.pack_start(h,False,False,6)
    self.gfxmode_c = c = gtk.CheckButton('%s  = %s' %(_("Set GFXMODE"), self.gfxmode))
    c.connect('toggled',self.set_gfxmode_cb)
    c.set_tooltip_markup(_('Enable this optin if you have boot trubles'))
    c.set_active(self.conf['GRUB_GFXMODE']=='800x600')
    h.pack_start(c, False,False,2)
    
    h=gtk.HBox(False,2); vbox.pack_start(h,False,False,6)
    l=gtk.Label("%s: '%s'" %(_("Font name"),self.font_fn))
    b = gtk.FontButton()
    b.connect('font-set', self.fc_match_cb, l)
    b.set_font_name(self.conf['FONT_NAME']  + ' 12')
    b.set_size_request(300,-1)
    h.pack_start(b, False,False,2)
    h.pack_start(l, False,False,2)
    
    # Apply buuton
    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    self.apply_b = b = gtk.Button(_('Apply'))
    b.connect('clicked', self.apply_cb)
    b.set_size_request(200,-1)
    h.pack_end(b, False,False,2)
    
    self.Time_Out.set_value(self.conf['GRUB_TIMEOUT'])
    self.Kernel_Opt.set_text(self.conf['GRUB_CMDLINE_LINUX'][1:-1])
    self.recovery_c.set_active(str(self.conf['GRUB_DISABLE_RECOVERY']).endswith('alse'))
    self.theme_c.set_active(True)
    #self.theme_c.set_active(self.conf.has_key('GRUB_BACKGROUND') and self.conf['GRUB_BACKGROUND'] != '')
    self.theme_c.set_active(os.path.isfile('/boot/grub2/unicode.pf2'))
    
  def update_theme_cb(self, b):
    self.tf.set_sensitive(b.get_active())

  def set_gfxmode_cb(self, b):
    if b.get_active():
      self.gfxmode='800x600'
    else:
      self.gfxmode='auto'
      
  def fc_match_cb(self, b, l):
    font=b.get_font_name().split()[:-1]
    font = ' '.join(font)
    fn = cmd_out("fc-match -f '%%{file}\n' '%s'" % font)[0]
    if os.path.splitext(fn)[1][1:] != 'ttf':
      b.set_font_name(self.font_nm + ' 12') 
      return error('%s (%s)' %(_('Error: Can not use this font!'),font),self.ccw)
    #print font, fn
    if os.path.isfile(fn):
      self.font_nm=font
      self.font_fn=fn
      l.set_text("%s: '%s'" %(_("Font name"),self.font_fn))
    
  def apply_cb(self, w):
    if not sure(_('Are you sure you want to changes?'), self.ccw): return
    dlg=wait()
    dlg.show_all()
    self.conf['GRUB_TIMEOUT'] = int(self.Time_Out.get_value())
    self.conf['GRUB_DISTRIBUTOR'] = self.conf['GRUB_DISTRIBUTOR']
    self.conf['GRUB_DISABLE_RECOVERY'] = str(not self.recovery_c.get_active()).lower()
    self.conf['GRUB_DEFAULT'] = self.conf['GRUB_DEFAULT']
    self.conf['GRUB_CMDLINE_LINUX'] = '"' + self.Kernel_Opt.get_text() + '"'
    self.conf['GRUB_GFXMODE'] = self.gfxmode
    self.conf['GRUB_GFXPAYLOAD_LINUX'] = "keep"
    self.conf['GRUB_BACKGROUND'] = self.bg_fn
    self.conf['FONT_FILE'] = self.font_fn
    self.conf['FONT_NAME'] = self.font_nm.replace(' ','_')
    font=self.font_fn
    if not self.theme_c.get_active():
    # grub2-mkconfig will ignore those options if /boot/grub2/unicode.pf2 not found
    #  del (self.conf['GRUB_GFXMODE'], self.conf['GRUB_GFXPAYLOAD_LINUX'], self.conf['GRUB_BACKGROUND'])
      font=''
    s = '\n'.join(map(lambda k: "%s=%s" % (k,str(self.conf[k])), self.conf.keys()))
    s +='\n'
    #print s,font
    #return
    r = self.ccw.mechanism('grub2', 'apply_cfg', self.conf_fn, s, font)
    dlg.hide()
    if r == 'NotAuth': return 
    if r.startswith("Error"): return error('%s: %s' %(_('Error!'),r),self.ccw)
    info(_('Done!'),self.ccw)
    
  def load_conf(self):
    s=''
    if os.path.exists(self.conf_fn):
      try: s=open(self.conf_fn,'rt').read()
      except OSError: pass
    self.parse_conf(s)
    try: self.conf['GRUB_TIMEOUT'] = int(self.conf['GRUB_TIMEOUT'])
    except ValueError:self.conf['GRUB_TIMEOUT'] = 5

  def parse_conf(self, s):
    self.default_conf()
    l1=map(lambda k: k.split('=',1), filter(lambda j: j,map(lambda i: i.strip(),s.splitlines())) )
    l2=map(lambda a: (a[0].strip(),a[1].strip()),filter(lambda j: len(j)==2,l1))
    r=dict(l2)
    self.conf.update(dict(l2))
    return len(l1)==len(l2)

  def default_conf(self):
    self.conf = {}
    self.conf['GRUB_TIMEOUT'] = 0
    self.conf['GRUB_DISTRIBUTOR'] = "Fedora"
    self.conf['GRUB_DISABLE_RECOVERY'] = "false"
    self.conf['GRUB_DEFAULT'] = "saved"
    self.conf['GRUB_CMDLINE_LINUX'] = '''"rd.md=0 rd.lvm=0 rd.dm=0  KEYTABLE=us quiet SYSFONT=latarcyrheb-sun16 rhgb rd.luks=0 LANG=en_US.UTF-8"'''
    self.conf['GRUB_GFXMODE'] = self.gfxmode
    self.conf['GRUB_GFXPAYLOAD_LINUX'] = "keep"
    self.conf['GRUB_BACKGROUND'] = self.bg_fn
    self.conf['FONT_FILE'] = self.font_fn
    self.conf['FONT_NAME'] = self.font_nm

