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

from gi.repository import Gtk, Gdk, GObject, GdkPixbuf
import os.path
from utils import *
import multiprocessing, time, signal

class NiceImage(Gtk.Image):
    def __init__(self, filename=None, icon=None,stock=None, iconsize=4):
        Gtk.Image.__init__(self)
        if filename: self.set_from_file(filename)
        elif icon: self.set_from_icon_name(icon, iconsize)
        elif stock: self.set_from_stock(stock, iconsize)

class NiceButton(Gtk.Button):
    def __init__(self, caption, img_fn=None, icon=None,stock=None):
        Gtk.Button.__init__(self,caption)
        self.set_size_request(100,100)
        self.set_image(NiceImage(img_fn, icon,stock))
        
def create_css_view():
        ###############################
        ## Not used :(
        display = Gdk.Display.get_default()
        screen = display.get_default_screen()
        css_provider = Gtk.CssProvider()
        #http://gnomejournal.org/article/107/styling-gtk-with-css
        #transition: 300ms ease-out;
        cssdate = """
                                ScrolledWindow, GtkViewport, MainButton {
                                        background-color: #eee;
                                        }
                                GtkWindow {
                                        background-color: #abb;
                                        background-image: -gtk-gradient (linear,
                                                                        left top, left bottom,
                                                                        from (#abb),
                                                                        to (shade (#fff, 0.5)));
                                        border-radius: 2px;
                                        border-width: 10px;
                                        margin: 55px;
                                        padding: 55px;
                                        }
                                    .notebook,
                            .entry {
                                        border-width: 0;
                                        background-image: -gtk-gradient (linear,
                                                                                                        left top, left bottom,
                                                                                                        from (#abb),
                                                                                                        to (shade (#eee, 0.9)));
                                        border-radius: 10px;
                                        border-style: solid;
                                        border-width: 5px;
                                        color: #000;
    }
                            """
        css_provider.load_from_data(cssdate)
        context = Gtk.StyleContext()
        context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
create_css_view()
class MainButton_(Gtk.Label):
    #__gtype_name__ = 'MainButton'
    ###############################
    ## Not used :(
    def __init__(self, caption, img_fn=None, icon=None, stock=None, iconsize=6):
        #super(MainButton, self).__init__()
        Gtk.Label.__init__(self, '<a href=".">%s</a>' % caption)
        self.set_use_markup(True)
        self.set_use_underline(False)
        self.set_line_wrap(True)
        self.set_justify(Gtk.Justification.CENTER)
        self.set_size_request(100,100)
        #ni = NiceImage(img_fn, icon, stock, iconsize)
        #self.add(ni)

class MainButton(Gtk.EventBox):
    __gtype_name__ = 'MainButton'
    def __init__(self, caption, img_fn=None, icon=None, stock=None, iconsize=6):
        #super(MainButton, self).__init__()
        self.caption = caption
        Gtk.EventBox.__init__(self)
        l = Gtk.Label(caption)
        l.set_line_wrap(True)
        l.set_justify(Gtk.Justification.CENTER)
        l.set_size_request(80,80)
        l.set_use_underline(False)
        ni = NiceImage(img_fn, icon, stock, iconsize)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(box)
        box.pack_start(ni, False,False, 1)
        box.pack_start(l, False,False, 1)
        self.set_size_request(100,100)
        self.set_resize_mode(0)
        #print self.get_children(), self
        #l.set_label(caption)
        
class MainButton_(Gtk.LinkButton):
    ###############################
    ## Not used :(
    def __init__(self, caption, img_fn=None, icon=None, stock=None, iconsize=6):
        #super(MainButton, self).__init__()
        Gtk.LinkButton.__init__(self,    '<a href=".">%s</a>' % caption, caption)
        self.set_use_underline(False)
        l = self.get_children()[0]
        l.set_line_wrap(True)
        l.set_justify(Gtk.Justification.CENTER)
        l.set_size_request(80,80)
        l.set_use_underline(False)
        ni = NiceImage(img_fn, icon, stock, iconsize)
        self.set_image(ni)
        self.set_image_position(2)

        self.set_size_request(100,100)
        #l.set_label(caption)

class MainButton_(Gtk.Button):
    __gtype_name__ = 'MainButton_'
    def __init__(self, caption, img_fn=None, icon=None, stock=None, iconsize=6):
        Gtk.Button.__init__(self)
        #self.set_size_request(80,80)
        self.set_focus_on_click(False)
        l=Gtk.Label.new(caption)
        #l.set_markup('<span color="blue">%s</span>' %caption)
        l.set_line_wrap(True)
        l.set_justify(Gtk.Justification.CENTER)
        l.set_width_chars(10)
        #l.set_size_request(80,50)
        #f = Gtk.Fixed()
        #f.add(l)
        #f.set_size_request(70,-1)
        ni = NiceImage(img_fn, icon, stock, iconsize)
        vbox=Gtk.VBox(False,2)
        #hbox=Gtk.HBox(True,2)
        #hbox.pack_start(f, True, True,6)
        vbox.pack_start(ni,False,False,6)
        vbox.pack_start(l,False,False,6)
        self.add(vbox)
        self.show_all()
        self.set_size_request(100, 100)
        #l.set_size_request(80,50)
        #self.chg_color()
        
    def chg_color(self):
        for i in range(5):
            self.modify_fg(Gtk.StateType(i), Gdk.color_parse("#ff0000"))

class CatFrame(Gtk.Frame):
    __gtype_name__ = 'OCC_CategoryFrame'
    # each element is category_id, category_caption, icon_id, category_tip
    def __init__(self, category, caption=None, icon=None, description=''):
        self.description = description
        if caption:
            self.caption = caption
        else:
            self.caption = category
        self.category = category
        #if icon:
        #    icon=getSpecialIcon(icon)
        Gtk.Frame.__init__(self)
        self.set_label(caption)
        self.set_border_width(6)
        self.set_shadow_type(Gtk.ShadowType(1))
        l=Gtk.Label(caption)
        #l.add(icon)
        #l.set_markup('<span color="blue">%s %s</span>' %(caption, '-' * (100-len(caption))))
        #l.set_markup('<span color="blue">%s</span>\n%s\n' % (caption, description))
        l.set_markup('<span color="blue">%s</span>\n' % (caption))
        h = Gtk.Box()
        #ni = NiceImage(icon=icon, iconsize=5)
        #h.pack_start(ni, False, False, 1)
        h.pack_start(l, False, False, 1)
        self.set_label_widget(h)
        self.vb = vb = Gtk.VBox(False,2)
        self.add(vb)
        #if description:
        #    h=Gtk.HBox(False,2)
        #    l=Gtk.Label(description)
        #    h.pack_start(l, False, False, 4)
        #    vb.pack_start(h, False, False, 4)
        self.show_all()
        
    def pack_start(self, w, *args):
        if args:
            self.vb.pack_start(w, *args)
        else:
            self.vb.pack_start(w, False, False, 4)
            
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

def wait(parent=None, msg='Please wait...', sec_msg=''):
    dlg = waitDialog(parent, msg)
    #dlg.present()
    #while(Gtk.main_iteration()): pass

    return dlg

def getSpecialIcon(icon,size=Gtk.IconSize.DIALOG):
    return Gtk.Image.new_from_icon_name(icon, size)
