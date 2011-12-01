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
import os.path
import logging
import gtk 
from OjubaControlCenter.pluginsClass import PluginsClass
from OjubaControlCenter.gwidgets import resetButton, GSCheckButton, comboBox, comboBoxWithFolder, creatVBox
from OjubaControlCenter.widgets import InstallOrInactive

class occPlugin(PluginsClass):
  def __init__(self,ccw):
    PluginsClass.__init__(self, ccw,_('Interface'),'gnome',50)
    description=_("Adjust interface settings")
    creatVBox(self, ccw, description, self.GioSettings) 
    
  def GioSettings(self, vb, ccw):
    P='org.gnome.desktop.interface'
    if not P in ccw.GSchemas_List: return False
    GS = ccw.GSettings(P)
    FB_l=( \
       (_('Menus have icons'),'menus-have-icons'),
       (_('Buttons have icons'),'buttons-have-icons')
    )
    for t,k in FB_l:
      b=GSCheckButton(t,k,GS)
      vb.pack_start(b,False,False,1)
    PP="org.gnome.shell.extensions.user-theme"
    b=InstallOrInactive(self, 'Install Gnome shell extension user theme','Gnome shell extension user theme installed','Package used to change Gnome shell theme',['gnome-shell-extension-user-theme'],'/usr/share/glib-2.0/schemas/org.gnome.shell.extensions.user-theme.gschema.xml')
    P_Stst=b.get_sensitive()
    if not P_Stst:
      GSP = ccw.GSettings(PP)
      cb=comboBoxWithFolder(_('Shell theme'),'name',GSP,self.get_shell_themes(),_('Add Shell theme'),os.path.expanduser('~/.themes'), self.get_shell_themes)
      vb.pack_start(cb,False,False,1)
    else:
      vb.pack_start(b,False,False,1)
    FD_l=( \
       (_('GTK+ theme'),'gtk-theme',self.get_gtk_themes(),_('Add GTK+ theme'),os.path.expanduser('~/.themes'), self.get_gtk_themes),
       (_('Icon theme'),'icon-theme',self.get_valid_icon_themes(),_('Add icons theme'),os.path.expanduser('~/.icons'), self.get_valid_icon_themes),
       (_('Cursor theme'),'cursor-theme',self.get_valid_cursor_themes(),_('Add cursor theme'),os.path.expanduser('~/.icons'), self.get_valid_cursor_themes)
    )
    for t,k,l,bt,dst,ls_func in FD_l:
      cb=comboBoxWithFolder(t,k,GS, l, bt, dst, ls_func)
      vb.pack_start(cb,False,False,1)
    return True
    
  def get_gtk_themes(self):
    """ Only shows themes that have variations for gtk+-3 and gtk+-2 """
    dirs = ( os.path.join('/usr/share/', "themes"),
             os.path.join(os.path.expanduser("~"), ".themes"))
    valid = self.walk_directories(dirs, lambda d:
             os.path.exists(os.path.join(d, "gtk-2.0")) and \
             os.path.exists(os.path.join(d, "gtk-3.0")))
    return valid
  
  def get_shell_themes(self):
    """ Only shows themes that have variations for gtk+-3 and gtk+-2 """
    dirs = ( os.path.join('/usr/share/', "themes"),
             os.path.join(os.path.expanduser("~"), ".themes"))
    valid = self.walk_directories(dirs, lambda d:
             os.path.exists(os.path.join(d, "gnome-shell")) and \
             os.path.exists(os.path.join(d, "gnome-shell", "gnome-shell.css")))
    valid.append('')
    return valid
    
  def get_valid_cursor_themes(self):
    dirs = ( os.path.join('/usr/share/', "icons"),
             os.path.join(os.path.expanduser("~"), ".icons"))
    valid = self.walk_directories(dirs, lambda d:
              os.path.isdir(d) and \
              os.path.exists(os.path.join(d, "cursors")))
    return valid
  
  def get_valid_icon_themes(self):
    dirs = ( os.path.join('/usr/share/', "icons"),
             os.path.join(os.path.expanduser("~"), ".icons"))
    valid = self.walk_directories(dirs, lambda d:
             os.path.isdir(d) and \
             not os.path.exists(os.path.join(d, "cursors")))
    return valid
    
  def walk_directories(self, dirs, filter_func):
    valid = []
    try:
        for thdir in dirs:
            if os.path.isdir(thdir):
                for t in os.listdir(thdir):
                    if filter_func(os.path.join(thdir, t)):
                         valid.append(t)
    except:
        logging.critical("Error parsing directories", exc_info=True)
    return valid
