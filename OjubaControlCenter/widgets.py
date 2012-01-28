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
import os.path
from utils import *

class NiceImage(gtk.Image):
  def __init__(self, filename=None, icon=None,stock=None):
    gtk.Image.__init__(self)
    if filename: self.set_from_file(filename)
    elif icon: self.set_from_icon_name(icon, gtk.ICON_SIZE_BUTTON)
    elif stock: self.set_from_stock(stock, gtk.ICON_SIZE_BUTTON)

class NiceButton(gtk.Button):
  def __init__(self, caption, img_fn=None, icon=None,stock=None):
    gtk.Button.__init__(self,caption)
    self.set_image(NiceImage(img_fn, icon,stock))

class LaunchFileButton(gtk.Button):
  def __init__(self, caption, fn):
    self.__fn=fn
    gtk.Button.__init__(self, caption)
    self.connect('clicked',self.__clicked)

  def __clicked(self,*args):
    if os.path.exists(self.__fn): run_in_bg("xdg-open '%s'" % self.__fn)
    else: error(_("File [%s] not found.") % self.__fn)

class LaunchButton(gtk.Button):
  def __init__(self, caption, cmd=None, fn=None, icon=None,stock=None):
    if not fn: fn=cmd
    elif not cmd: cmd=fn
    self.__cmd=cmd
    self.__fn=fn
    
    gtk.Button.__init__(self, caption)
    self.connect('clicked',self.__clicked)
    if self.__fn and not os.path.exists(self.__fn): self.set_sensitive(False); self.set_tooltip_text(_("not available"))
    if icon: self.set_image(gtk.image_new_from_icon_name(icon, gtk.ICON_SIZE_BUTTON))
    elif stock: self.set_image(gtk.image_new_from_stock(stock, gtk.ICON_SIZE_BUTTON))

  def __clicked(self,*args):
    run_in_bg(self.__cmd)

class LaunchFileManager(LaunchButton):
  def __init__(self, caption, path=None,**k):
    # if not path or not os.path.exists(path): 
    cmd=file_man_cmd(path)
    fn=which_exe(cmd.split(' ',1)[0])
    LaunchButton.__init__(self, caption, cmd, fn=fn, **k)

class LaunchOrInstall(gtk.Button):
  def __init__(self, plugin, caption, filename,pkgs=None,cmd=None):
    self.__plugin=plugin
    self.__fn=filename
    if type(pkgs)==str or type(pkgs)==unicode: pkgs=[pkgs]
    self.__pkgs=pkgs
    self.__cmd=cmd
    if not self.__cmd: self.__cmd=self.__fn
    gtk.Button.__init__(self, caption)
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

class InstallOrInactive(gtk.Button):
  def __init__(self, plugin, caption, caption_if_installed, tip, pkgs=[], fn=None):
    self.__plugin=plugin
    self.__pkgs=pkgs
    self.__c0=caption
    self.__c1=caption_if_installed
    self.__fn=fn
    gtk.Button.__init__(self, "foo")
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

class imgchooser(gtk.FileChooserButton):
  def __init__(self, title):
    gtk.FileChooserButton.__init__(self, title)
    self.preview = preview = gtk.Image()
    self.set_preview_widget(preview)
    self.connect("update-preview", self.update_preview_cb)
    ff=f=gtk.FileFilter()
    #ff.set_name(_('PNG image files'))
    #ff.add_mime_type('image/png')
    #fc.add_filter(ff)
    ff=gtk.FileFilter()
    ff.set_name(_('All image files'))
    ff.add_mime_type('image/*')
    self.set_filter(ff)
    
  def update_preview_cb(self, s=None, fn=None):
    filename = self.get_preview_filename()
    if fn and not filename: filename=fn
    try:
      pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(filename, 200, 200)
      self.preview.set_from_pixbuf(pixbuf)
      have_preview = True
    except:
      have_preview = False
    self.set_preview_widget_active(have_preview)

class sel_dir_dlg(gtk.FileChooserDialog):
  def __init__(self):
    gtk.FileChooserDialog.__init__(self,_("Select directory"), parent=self, buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
    self.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
    self.set_position(gtk.WIN_POS_CENTER)
    self.connect('delete-event', lambda w, *a: w.hide() or True)
    self.connect('response', lambda w, *a: w.hide() or True)
        
def sure(msg, win=None):
  dlg=gtk.MessageDialog(win,gtk.DIALOG_MODAL,gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, msg)
  dlg.connect("response", lambda *args: dlg.hide())
  r=dlg.run()
  dlg.destroy()
  return r==gtk.RESPONSE_YES

def info(msg, win=None):
  dlg=gtk.MessageDialog(win,gtk.DIALOG_MODAL,gtk.MESSAGE_INFO, gtk.BUTTONS_OK, msg)
  dlg.connect("response", lambda *args: dlg.hide())
  r=dlg.run()
  dlg.destroy()

def error(msg, win=None):
  dlg=gtk.MessageDialog(win,gtk.DIALOG_MODAL,gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, msg)
  dlg.connect("response", lambda *args: dlg.hide())
  r=dlg.run()
  dlg.destroy()

def wait(win=None):
  dlg=gtk.MessageDialog(win,gtk.DIALOG_MODAL,gtk.MESSAGE_INFO, 0, _("Please wait..."))
  dlg.connect("response", lambda *args: dlg.hide())
  dlg.show_all()
  while gtk.events_pending(): gtk.main_iteration_do()
  #gtk.main_iteration_do()
  #while(gtk.main_iteration_do()): pass
  return dlg

