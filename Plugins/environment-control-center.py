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
import os,random
from gi.repository import Gtk,GdkPixbuf
from OjubaControlCenter.pluginsClass import PluginsClass
from OjubaControlCenter.widgets import LaunchButton

## NOTE: these global vars is loader validators
category = 'desktop'
caption = _('Environment Control Center')
description = 'Environment Control Center'
priority = 10

class occPlugin(PluginsClass):
    def __init__(self,ccw):
        PluginsClass.__init__(self, ccw, caption, category, priority)
        self.location=os.path.dirname(os.path.abspath(__file__))[:-7]+"icons/"
        self.desktop=os.getenv("XDG_CURRENT_DESKTOP")
        
        self.gif_image=random.choice(["%stuxtricks.gif"%self.location,"%spanguin_bird_flying_red_animation_clipart.GIF"%self.location])
        
        self.desktop_cc={"GNOME"      :["Gnome","/usr/bin/gnome-control-center"],
                         "KDE"        :["Kde","/usr/bin/systemsettings5"] ,
                         "XFCE"       :["Xfce","/usr/bin/xfce4-settings-manager"] ,
                         "X-LXQt"     :["Lxqt","/usr/bin/lxqt-config"] ,
                         "X-Cinnamon" :["Cinnamon","/usr/share/cinnamon/cinnamon-settings/cinnamon-settings.py"] ,
                         "MATE"       :["Mate","/usr/bin/mate-control-center"] ,
                         "X-Hawaii"   :["Hawaii","/usr/bin/hawaii-system-preferences"]
                         } 
        
        self.lxde_cc=[ ["Customize Look and Feel","/usr/bin/lxappearance"] ,["Default Applications","/usr/bin/lxsession-default-apps"],["Desktop Session Settings","/usr/bin/lxsession-edit"] ,["Display Settings","/usr/bin/lxrandr"],["Windows Manager Configuration","/usr/bin/obconf"],["Input Device Preferences","/usr/bin/lxinput"]]
        
        vb=Gtk.VBox(False,2)
        self.add(vb)
        hb=Gtk.HBox(False,5)
        vb.pack_start(hb,True,True,10)
        vb1=Gtk.VBox(False,10)
        hb.pack_start(vb1,True,True,10)
        
        pixbuf=GdkPixbuf.PixbufAnimation.new_from_file(self.gif_image)
        image=Gtk.Image.new_from_animation(pixbuf)
        vb1.pack_start(image,True,True,0)
            
        if self.desktop=="":
            if os.getenv("DESKTOP_SESSION")=="/usr/share/xsessions/openbox":
                vb1.pack_start(LaunchButton(_('Openbox Manager Configuration'),'/usr/bin/obconf'),False,False,5)
            else:
                pass
        
        elif self.desktop=="LXDE":
            for i in self.lxde_cc:
                vb1.pack_start(LaunchButton(_(i[0]) , i[1] ) ,True,True,0)

        
        elif self.desktop=="GNOME":
            vb1.pack_start(LaunchButton(_('%s Control Center' %self.desktop_cc[ self.desktop ] [0] ),self.desktop_cc[ self.desktop ] [1]),True,True,0)
            
            if os.path.exists("/usr/bin/gnome-tweak-tool"):
                vb1.pack_start(LaunchButton(_('Gnome Tweak Tool'),'/usr/bin/gnome-tweak-tool'),False,False,5)
                vb.pack_start(hb,False,False,6)
        
        else:
            vb1.pack_start(LaunchButton(_('%s Control Center' %self.desktop_cc[ self.desktop ] [0] ),self.desktop_cc[ self.desktop ] [1]),True,True,0)


    
    
        






