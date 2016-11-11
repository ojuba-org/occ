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
import os,dnf
from gi.repository import Gtk
from OjubaControlCenter.pluginsClass import PluginsClass
from OjubaControlCenter.widgets import  error

#ملاحظة في فيدورا 25 و 24  تحتاج الإضافة حزمة python2-dnf-plugins-core لا أعلم عن باقي الإصدارات.
## NOTE: these global vars is loader validators
category = 'desktop'
caption = _('Manager repos')
description = _("Manager Repos")
priority = 100



class occPlugin(PluginsClass):
    def __init__(self,ccw):
        PluginsClass.__init__(self, ccw, caption, category, priority)

	self.base=dnf.Base()
	self.base.read_all_repos()
	self.allrepos=self.base.repos.all()
	
        self.count=0
        self.hbox=Gtk.HBox(spacing=20)
        self.add(self.hbox)
        self.vbox1=Gtk.VBox()
        self.vbox2=Gtk.VBox()
        self.grid=Gtk.Grid(row_homogeneous=True)
        self.vbox2.pack_start(self.grid,True,True,0)
        self.hbox.pack_start(self.vbox1,True,True,0)
        self.hbox.pack_start(self.vbox2,True,True,0)
        self.name_label=Gtk.Label(_("<b>Name</b>"),use_markup=True)
        self.vbox1.pack_start(self.name_label,True,True,0)
        self.execute_label=Gtk.Label(_("<b>Switch</b>"),use_markup=True)
        self.grid.attach(self.execute_label,0,self.count,1,1)
        self.count+=1
        
        
        
        
        for repo in self.allrepos:
            self.name=Gtk.Label(repo.name)
            if not repo.enabled:
                self.switch=Gtk.Switch()
            else:
                self.switch=Gtk.Switch()
                self.switch.set_active(True)
            
            self.switch.connect("state-set",self.__enable_or_disable,repo.hawkey_repo.name)
            self.vbox1.pack_start(self.name,True,True,0)
            self.grid.attach(self.switch,0,self.count,1,1)
            self.count+=1
			
			
    def __refresh_repos_informations(self):
        self.__reposinformations=self.__get_information_from_location()
    
    def __enable_or_disable(self,b,s,data):
        if not b.get_state():
            check=self.ccw.mechanism('run','system',"dnf config-manager --set-enable %s -y"%data)
            if check!='0':
                error(_("unexpected return code, possible an error had occurred"), self.ccw)
                b.set_state(False)
                b.set_active(False)
                return True
                
            
        else:
            check=self.ccw.mechanism('run','system',"dnf config-manager --set-disable %s -y"%data)
            if check!='0':
                error(_("unexpected return code, possible an error had occurred"), self.ccw)
                b.set_state(True)
                b.set_active(True)
                return True

