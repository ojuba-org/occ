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

from gi.repository import Gtk, Gdk, GObject, GdkPixbuf
import os.path
from utils import *
import multiprocessing, time, signal

class NiceImage(Gtk.Image):
  def __init__(self, filename=None, icon=None,stock=None):
    Gtk.Image.__init__(self)
    if filename: self.set_from_file(filename)
    elif icon: self.set_from_icon_name(icon, Gtk.IconSize.BUTTON)
    elif stock: self.set_from_stock(stock, Gtk.IconSize.BUTTON)

class NiceButton(Gtk.Button):
  def __init__(self, caption, img_fn=None, icon=None,stock=None):
    Gtk.Button.__init__(self,caption)
    self.set_image(NiceImage(img_fn, icon,stock))

class LaunchFileButton(Gtk.Button):
  def __init__(self, caption, fn):
    self.__fn=fn
    Gtk.Button.__init__(self, caption)
    self.connect('clicked',self.__clicked)

  def __clicked(self,*args):
    if os.path.exists(self.__fn): run_in_bg("xdg-open '%s'" % self.__fn)
    else: error(_("File [%s] not found.") % self.__fn)

class LaunchButton(Gtk.Button):
  def __init__(self, caption, cmd=None, fn=None, icon=None,stock=None):
    if not fn: fn=cmd
    elif not cmd: cmd=fn
    self.__cmd=cmd
    self.__fn=fn
    
    Gtk.Button.__init__(self, caption)
    self.connect('clicked',self.__clicked)
    if self.__fn and not os.path.exists(self.__fn): self.set_sensitive(False); self.set_tooltip_text(_("not available"))
    if icon: self.set_image(Gtk.Image.new_from_icon_name(icon, Gtk.IconSize.BUTTON))
    elif stock: self.set_image(Gtk.Image.new_from_stock(stock, Gtk.IconSize.BUTTON))

  def __clicked(self,*args):
    run_in_bg(self.__cmd)

class LaunchFileManager(LaunchButton):
  def __init__(self, caption, path=None,**k):
    # if not path or not os.path.exists(path): 
    cmd=file_man_cmd(path)
    fn=which_exe(cmd.split(' ',1)[0])
    LaunchButton.__init__(self, caption, cmd, fn=fn, **k)

class LaunchOrInstall(Gtk.Button):
  def __init__(self, plugin, caption, filename,pkgs=None,cmd=None):
    self.__plugin=plugin
    self.__fn=filename
    if type(pkgs)==str or type(pkgs)==unicode: pkgs=[pkgs]
    self.__pkgs=pkgs
    self.__cmd=cmd
    if not self.__cmd: self.__cmd=self.__fn
    Gtk.Button.__init__(self, caption)
    self.connect('clicked',self.__clicked)

  def __run(self):
    run_in_bg(self.__cmd)
    return True
  def __install(self):
      if not self.__pkgs: r=self.__plugin.install_by_file(self.__fn)
      else: r=self.__plugin.ccw.install_packages(self.__pkgs)
  def is_installed(self, full_check=True):
    if not full_check: return os.path.exists(self.__fn)
    self.__plugin.ccw.is_installed(self.__pkgs)
  def __clicked(self,*args):
    r=os.path.exists(self.__fn) and self.__run() or self.__install()

class InstallOrInactive(Gtk.Button):
  def __init__(self, plugin, caption, caption_if_installed, tip, pkgs=[], fn=None):
    self.__plugin=plugin
    self.__pkgs=pkgs
    self.__c0=caption
    self.__c1=caption_if_installed
    self.__fn=fn
    Gtk.Button.__init__(self, "foo")
    self.set_sensitive(True)
    self.set_tooltip_markup(tip)
    self.connect('clicked',self.__clicked)
    #self.__plugin.load_ls.append(self.load_cb)
    self.load_cb()
  
  def is_installed(self):
    if self.__fn: return os.path.exists(self.__fn)
    else: return self.__plugin.ccw.is_installed(self.__pkgs)
  
  def load_cb(self):
    if self.is_installed():
      self.set_sensitive(False)
      self.set_label(self.__c1)
    else:
      self.set_sensitive(True)
      self.set_label(self.__c0)

  def __clicked(self,*args):
    self.__plugin.ccw.install_packages(self.__pkgs)

class imgchooser(Gtk.FileChooserDialog):
  def __init__(self, title, fn=None, parent=None):
    Gtk.FileChooserDialog.__init__(self, title, parent,
                                  Gtk.FileChooserAction.OPEN,
                                   (
                                    Gtk.STOCK_CANCEL,
                                    Gtk.ResponseType.CANCEL,
                                    Gtk.STOCK_OPEN, Gtk.ResponseType.OK
                                   )
                                  )
    self.preview = preview = Gtk.Image()
    self.set_preview_widget(preview)
    self.connect("update-preview", self.update_preview_cb)
    ff=f=Gtk.FileFilter()
    #ff.set_name(_('PNG image files'))
    #ff.add_mime_type('image/png')
    #fc.add_filter(ff)
    ff=Gtk.FileFilter()
    ff.set_name(_('All image files'))
    ff.add_mime_type('image/*')
    self.set_filter(ff)
    self.set_filename(fn)
    self.update_preview_cb(fn=fn)
    
  def update_preview_cb(self, s=None, fn=None):
    filename = self.get_preview_filename()
    if fn and not filename: filename=fn
    try:
      pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(filename, 200, 200)
      self.preview.set_from_pixbuf(pixbuf)
      have_preview = True
    except Exception:
      have_preview = False
    self.set_preview_widget_active(have_preview)

class sel_dir_dlg(Gtk.FileChooserDialog):
  def __init__(self, parent=None):
    Gtk.FileChooserDialog.__init__(self,_("Select directory"), parent=parent, buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT, Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT))
    self.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
    #self.set_position(Gtk.WIN_PositionType.CENTER)
    self.connect('delete-event', lambda w, *a: w.hide() or True)
    self.connect('response', lambda w, *a: w.hide() or True)
        
class MessageDialog(Gtk.MessageDialog):
  MsgTypes={
              'sure': [Gtk.MessageType.QUESTION, Gtk.ButtonsType.YES_NO],
              'info': [Gtk.MessageType.INFO, Gtk.ButtonsType.OK], 
              'error': [Gtk.MessageType.ERROR, Gtk.ButtonsType.CLOSE],
              'wait': [Gtk.MessageType.OTHER ,Gtk.ButtonsType.NONE]
            }
  def __init__(self, msg_type, sec_text, parent, text=''):
    msg=None
    if not msg_type == 'wait': msg=sec_text
    Gtk.MessageDialog.__init__(self, parent , 1, self.MsgTypes[msg_type][0],
                               self.MsgTypes[msg_type][1], text)
    self.format_secondary_text(msg)
    if msg_type == 'wait':
      c = self.get_message_area()
      self.p = p = Gtk.ProgressBar()
      p.set_text(text)
      p.set_show_text(True)
      c.add(p)
      self.show_all
      GObject.timeout_add(20, self.update_progrss)
  
  def update_progrss(self):
    self.p.pulse()
    return True

class waitDialog(Gtk.Dialog):
  def __init__(self, parent, text):
    Gtk.Dialog.__init__(self,text, parent, 1)
    #self.connect("delete-event", self.on_close )
    #self.connect("destroy", self.on_close)
    #self.set_parent(parent)
    c = self.get_content_area()
    self.p = p = Gtk.ProgressBar()
    p.set_text(text)
    p.set_show_text(True)
    c.add(p)
    self.show_all()
    GObject.timeout_add(20, self.update_progrss)
  
  def update_progrss(self):
    self.p.pulse()
    return True
  
  def on_close(self, *w):
    return True
    
def sure(msg, parent=None, sec_msg=''):
  dlg = MessageDialog('sure', msg, parent, sec_msg)
  r = dlg.run()
  dlg.destroy()
  return r==Gtk.ResponseType.YES

def info(msg, parent=None, sec_msg=''):
  dlg = MessageDialog('info', msg, parent, sec_msg)
  r = dlg.run()
  dlg.destroy()
  return True

def error(msg, parent=None, sec_msg=''):
  dlg = MessageDialog('error', msg, parent, sec_msg)
  r = dlg.run()
  dlg.destroy()
  return True

def wait(parent=None, msg=_('Please wait...'), sec_msg=''):
  dlg = waitDialog(parent, msg)
  #dlg.present()
  #while(Gtk.main_iteration()): pass

  return dlg


