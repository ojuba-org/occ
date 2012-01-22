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
from OjubaControlCenter.utils import cmd_out, copyfile
from OjubaControlCenter.widgets import InstallOrInactive, sure, info, error, wait, imgchooser
from OjubaControlCenter.pluginsClass import PluginsClass

class occPlugin(PluginsClass):
  conf={}
  conf[0]={}
  conf[1]={}
  conf_fn='/etc/default/grub'
  user_conf=os.path.join(os.path.expanduser('~'),'.occ','grub')
  font_fn='/usr/share/fonts/dejavu/DejaVuSansMono.ttf'
  font_nm='Sans'
  bg_nm='/tmp/grubbg.png' #os.path.join(os.path.expanduser('~'),'.occ','grub2.png')
  bg_fn='/usr/share/backgrounds/verne/default/normalish/verne.png'
  gfxmode='auto'
  def __init__(self,ccw):
    PluginsClass.__init__(self, ccw,_('Grub2 settings:'),'boot',30)
    vb=gtk.VBox(False,2)
    self.add(vb)
    if not ccw.installed_info('grub2'): 
      h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
      l=gtk.Label(_("Grub2 not isntalled!"))
      h.pack_start(l, False,False,2)
      return
    self.default_conf()
    self.load_conf(0,self.conf_fn)
    self.load_conf(1,self.user_conf)
    cfg_dir=os.path.dirname(self.user_conf)
    if os.path.isfile(cfg_dir): os.unlink(cfg_dir)
    if not os.path.exists(cfg_dir): os.mkdir(cfg_dir)
    

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
    
    if os.path.isfile(self.conf[1]['FONT_FILE']): self.font_fn=self.conf[1]['FONT_FILE']
    self.font_nm = self.conf[1]['FONT_NAME']
    self.gfxmode = self.conf[0]['GRUB_GFXMODE']
    self.bg_fn = self.conf[1]['BACKGROUND']
    # Grub2 theme frame
    self.tf = f = gtk.Frame(_('Grub2 Theme:')); vb.pack_start(f,False,False,6)
    vbox = gtk.VBox(False,2)
    f.add(vbox)
    
    h=gtk.HBox(False,2); vbox.pack_start(h,False,False,6)
    l=gtk.Label(_("This section will help you to change grub2 Font and background (theme)."))
    h.pack_start(l, False,False,2)
    
    h=gtk.HBox(False,2); vbox.pack_start(h,False,False,6)
    l=gtk.Label("%s: %s" %(_("Background"),self.bg_fn))
    #b=gtk.Button(_('Change picture'))
    #b.connect('clicked', self.open_pic_cb, l)
    #h.pack_start(b, False,False,2)
    fc=imgchooser(_('Choose boot background'))
    if self.conf[1].has_key('BACKGROUND') and os.path.exists(self.conf[1]['BACKGROUND']):
      fc.set_filename(self.conf[1]['BACKGROUND'])
      fc.update_preview_cb(fn=self.conf[1]['BACKGROUND'])
    fc.connect('file-set', self.img_changed, l)
    h.pack_start(fc, False,False,2)
    h.pack_start(l, False,False,2)
    
    h=gtk.HBox(False,2); vbox.pack_start(h,False,False,6)
    self.img=img=gtk.Image()
    #self.img_preview()
    h.pack_start(img, False, False, 2)
    self.img_preview()
    
    h=gtk.HBox(False,2); vbox.pack_start(h,False,False,6)
    self.gfxmode_c = c = gtk.CheckButton('%s  = %s' %(_("Set GFXMODE"), self.gfxmode))
    c.connect('toggled',self.set_gfxmode_cb)
    c.set_tooltip_markup(_('Enable this option if you have boot troubles\n\nIf your monitor got out sync or turned off, While grub2 menu\nPress enter to continue booting, And enable this option.'))
    c.set_active(self.conf[0]['GRUB_GFXMODE']=='800x600')
    h.pack_start(c, False,False,2)
    
    h=gtk.HBox(False,2); vbox.pack_start(h,False,False,6)
    l=gtk.Label("%s: %s" %(_("Font name"),self.font_fn))
    b = gtk.FontButton()
    b.connect('font-set', self.fc_match_cb, l)
    b.set_font_name(self.conf[1]['FONT_NAME']  + ' 12')
    b.set_size_request(300,-1)
    h.pack_start(b, False,False,2)
    h.pack_start(l, False,False,2)
    
    # Apply buuton
    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    self.apply_b = b = gtk.Button(_('Apply'))
    b.connect('clicked', self.apply_cb)
    b.set_size_request(200,-1)
    h.pack_end(b, False,False,2)
    self.Time_Out.set_value(self.conf[0]['GRUB_TIMEOUT'])
    self.Kernel_Opt.set_text(self.conf[0]['GRUB_CMDLINE_LINUX'][1:-1])
    self.recovery_c.set_active(not self.conf[0]['GRUB_DISABLE_RECOVERY']=='true')
    self.theme_c.set_active(True)
    #self.theme_c.set_active(self.conf.has_key('GRUB_BACKGROUND') and self.conf['GRUB_BACKGROUND'] != '')
    self.theme_c.set_active(os.path.isfile('/boot/grub2/unicode.pf2'))
    
  def img_preview(self, fn=None):
    if not fn:
      if not self.conf[1].has_key('BACKGROUND'): return False
      fn=self.conf[1]['BACKGROUND']
    # FIXME: show broken image instead of return
    if not os.path.exists(fn): return False
    W=gtk.gdk.screen_width()
    H=gtk.gdk.screen_height()
    try: pixbuf = gtk.gdk.pixbuf_new_from_file(fn)
    except: return False
    scaled_buf = pixbuf.scale_simple(int(W*128/H),128,gtk.gdk.INTERP_BILINEAR)
    self.img.set_from_pixbuf(scaled_buf)
    return True
    
  def convert_img(self, in_fn, out_fn, t='png'):
    if not os.path.isfile(in_fn):
      self.bg_nm=''
      return
    try:
      im=gtk.gdk.pixbuf_new_from_file(in_fn)
      im.save(out_fn, t)
    except:
      self.bg_nm=''
    
  def img_changed(self, b,l):
    fn=b.get_filename()
    if not self.img_preview(fn): return
    self.bg_fn=fn
    l.set_text("%s: %s" %(_("Background"),self.bg_fn))
    
  def png_match(self, fn):
    if not os.path.isfile(fn): return False
    f = ' '.join(cmd_out("file \"%s\"" % fn)[0].split(':')[1].split()[0:-1])
    if 'PNG image data' in f and '8-bit/color RGBA' in f : return True
    return False
    
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
      l.set_text("%s: %s" %(_("Font name"),self.font_fn))
    
  def apply_cb(self, w):
    if not sure(_('Are you sure you want to apply changes?'), self.ccw): return
    dlg=wait(self.ccw)
    dlg.show_all()
    self.convert_img(self.bg_fn, self.bg_nm)
    self.conf[0]['GRUB_TIMEOUT'] = int(self.Time_Out.get_value())
    self.conf[0]['GRUB_DISTRIBUTOR'] = self.conf[0]['GRUB_DISTRIBUTOR']
    self.conf[0]['GRUB_DISABLE_RECOVERY'] = str(not self.recovery_c.get_active()).lower()
    self.conf[0]['GRUB_DEFAULT'] = self.conf[0]['GRUB_DEFAULT']
    self.conf[0]['GRUB_CMDLINE_LINUX'] = '"' + self.Kernel_Opt.get_text() + '"'
    self.conf[0]['GRUB_GFXMODE'] = self.gfxmode
    self.conf[0]['GRUB_GFXPAYLOAD_LINUX'] = "keep"
    self.conf[0]['GRUB_BACKGROUND'] = '/boot/grub2/oj.grub2.png'
    self.conf[1]['BACKGROUND'] = self.bg_fn
    self.conf[1]['FONT_FILE'] = self.font_fn
    self.conf[1]['FONT_NAME'] = self.font_nm
    font=self.font_fn
    if not self.theme_c.get_active(): font=''
    cfg = '\n'.join(map(lambda k: "%s=%s" % (k,str(self.conf[0][k])), self.conf[0].keys()))
    cfg +='\n'
    usr_cfg = '\n'.join(map(lambda k: "%s=%s" % (k,str(self.conf[1][k])), self.conf[1].keys()))
    try: open(self.user_conf, 'w+').write(usr_cfg)
    except IOError: pass
    #print usr_cfg, '\n\n',cfg,font, self.bg_fn,self.bg_nm
    #return
    r = self.ccw.mechanism('grub2', 'apply_cfg', self.conf_fn, cfg, font, self.bg_nm)
    dlg.hide()
    if r == 'NotAuth': return 
    if r.startswith("Error"): return error('%s: %s' %(_('Error!'),r),self.ccw)
    info(_('Done!'),self.ccw)

  def load_conf(self,n,fn):
    s=''
    if os.path.exists(fn):
      try: s=open(fn,'rt').read()
      except OSError: pass
    self.parse_conf(s,n)
    try: self.conf[0]['GRUB_TIMEOUT'] = int(self.conf[0]['GRUB_TIMEOUT'])
    except ValueError:self.conf[0]['GRUB_TIMEOUT'] = 5

  def parse_conf(self, s,n):
    l1=map(lambda k: k.split('=',1), filter(lambda j: j,map(lambda i: i.strip(),s.splitlines())) )
    l2=map(lambda a: (a[0].strip(),a[1].strip()),filter(lambda j: len(j)==2,l1))
    r=dict(l2)
    self.conf[n].update(dict(l2))
    return len(l1)==len(l2)

  def default_conf(self):
    self.conf={}
    self.conf[0] = {}
    self.conf[1] = {}
    self.conf[0]['GRUB_TIMEOUT'] = 0
    self.conf[0]['GRUB_DISTRIBUTOR'] = "Fedora"
    self.conf[0]['GRUB_DISABLE_RECOVERY'] = "false"
    self.conf[0]['GRUB_DEFAULT'] = "saved"
    self.conf[0]['GRUB_CMDLINE_LINUX'] = '''"rd.md=0 rd.lvm=0 rd.dm=0  KEYTABLE=us quiet SYSFONT=latarcyrheb-sun16 rhgb rd.luks=0 LANG=en_US.UTF-8"'''
    self.conf[0]['GRUB_GFXMODE'] = self.gfxmode
    self.conf[0]['GRUB_GFXPAYLOAD_LINUX'] = "keep"
    self.conf[0]['GRUB_BACKGROUND'] = '/boot/grub2/oj.grub2.png'
    self.conf[1]['BACKGROUND'] = self.bg_fn
    self.conf[1]['FONT_FILE'] = self.font_fn
    self.conf[1]['FONT_NAME'] = self.font_nm

