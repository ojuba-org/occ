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
import os
import subprocess
from gi.repository import Gtk
from OjubaControlCenter.pluginsClass import PluginsClass
from OjubaControlCenter.widgets import  error


## NOTE: these global vars is loader validators
category = 'desktop'
caption = _('Services Manager')
description = _("Services Manager")
priority = 100



class occPlugin(PluginsClass):
    def __init__(self,ccw):
        PluginsClass.__init__(self, ccw, caption, category, priority)
	self.__allservices= subprocess.Popen("LANG=C TERM=dumb COLUMNS=1024 systemctl list-unit-files  --all --type service --no-legend --no-pager --no-ask-password",stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).communicate()[0].decode('utf-8').strip().split()

	self.__all_ss_services= subprocess.Popen("LANG=C TERM=dumb COLUMNS=1024 systemctl list-units  --all --type service --no-legend --no-pager --no-ask-password",stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).communicate()[0].decode('utf-8').strip().split("\n")
	self.__ss_black_list=("dbus.service","gdm.service","lightdm.service","kdm.service","sddm.service","mdm.service","upower.service","udisks2.service")
	self.__black_list=("dbus.service","gdm.service","lightdm.service","kdm.service","sddm.service","mdm.service","upower.service","udisks2.service")

	self.__all_enabled_disabled_services=self.__get_enabled_disabled_service()
	self.__all_start_stop_services=self.__get_start_stop_service()

        self.count=0
	self.count1=0

	self.notebook=Gtk.Notebook()
	self.add(self.notebook)
	
	self.page1=Gtk.HBox()
	self.page1.set_border_width(10)
	self.label1=Gtk.Label(_("Enable/Disable"))
	self.notebook.append_page(self.page1,self.label1)	
	
	self.page2=Gtk.HBox()
	self.page2.set_border_width(10)
	self.label2=Gtk.Label(_("Start/Stop"))
	self.notebook.append_page(self.page2,self.label2)

        self.vbox1=Gtk.VBox()
        self.vbox2=Gtk.VBox()
	
        self.vbox3=Gtk.VBox()
        self.vbox4=Gtk.VBox()
	
        self.grid=Gtk.Grid(row_homogeneous=True)
        self.vbox2.pack_start(self.grid,True,True,0)
        self.page1.pack_start(self.vbox1,True,True,0)
        self.page1.pack_start(self.vbox2,True,True,0)
        self.name_label=Gtk.Label(_("<b>Name</b>"),use_markup=True)
        self.vbox1.pack_start(self.name_label,True,True,0)
        self.execute_label=Gtk.Label(_("<b>Switch</b>"),use_markup=True)
        self.grid.attach(self.execute_label,0,self.count,1,1)
        self.count+=1
        
        self.grid1=Gtk.Grid(row_homogeneous=True)
        self.vbox4.pack_start(self.grid1,True,True,0)
        self.page2.pack_start(self.vbox3,True,True,0)
        self.page2.pack_start(self.vbox4,True,True,0)
        self.name_label1=Gtk.Label(_("<b>Name</b>"),use_markup=True)
        self.vbox3.pack_start(self.name_label1,True,True,0)
        self.execute_label1=Gtk.Label(_("<b>Switch</b>"),use_markup=True)
        self.grid1.attach(self.execute_label1,0,self.count1,1,1)
        self.count1+=1
        
        
        for service in self.__all_enabled_disabled_services:
            self.name=Gtk.Label(service[0][:-8])
            if  service[1]=="disabled":
                self.switch=Gtk.Switch()
            else:
                self.switch=Gtk.Switch()
                self.switch.set_active(True)
            
            self.switch.connect("state-set",self.__enable_or_disable,service[0])
            self.vbox1.pack_start(self.name,True,True,0)
            self.grid.attach(self.switch,0,self.count,1,1)
            self.count+=1
			
        for service in self.__all_start_stop_services:
            self.name1=Gtk.Label(service[0][:-8])
            if  service[1]=="dead":
                self.switch1=Gtk.Switch()
            else:
                self.switch1=Gtk.Switch()
                self.switch1.set_active(True)
            
            self.switch1.connect("state-set",self.__start_or_stop,service[0])
            self.vbox3.pack_start(self.name1,True,True,0)
            self.grid1.attach(self.switch1,0,self.count1,1,1)
            self.count1+=1
    
    def __enable_or_disable(self,b,s,data):
        if not b.get_state():
            check=self.ccw.mechanism('run','system',"systemctl enable %s"%data)
            if check!='0':
                error(_("unexpected return code, possible an error had occurred"), self.ccw)
                b.set_state(False)
                b.set_active(False)
                return True
                
            
        else:
            check=self.ccw.mechanism('run','system',"systemctl disable %s"%data)
            if check!='0':
                error(_("unexpected return code, possible an error had occurred"), self.ccw)
                b.set_state(True)
                b.set_active(True)
                return True


    def __get_enabled_disabled_service(self):
	result=[]
	for service in self.__allservices:
		if service in self.__black_list:
			continue
		elif self.__allservices[self.__allservices.index(service)+1]=="enabled":
			result.append([service,"enabled"])
		elif self.__allservices[self.__allservices.index(service)+1]=="disabled":
			result.append([service,"disabled"])
			
	return result





    def __start_or_stop(self,b,s,data):
        if not b.get_state():
            check=self.ccw.mechanism('run','system',"systemctl start %s"%data)
            if check!='0':
                error(_("unexpected return code, possible an error had occurred"), self.ccw)
                b.set_state(False)
                b.set_active(False)
                return True
                
            
        else:
            check=self.ccw.mechanism('run','system',"systemctl stop %s"%data)
            if check!='0':
                error(_("unexpected return code, possible an error had occurred"), self.ccw)
                b.set_state(True)
                b.set_active(True)
                return True

    def __filter_result(self,out):
	result=[]
	for line in out:
		line=line.split()
		result.append([line[0],line[3]])
	return result

    def __get_start_stop_service(self):
	result=[]
	services=self.__filter_result(self.__all_ss_services)
	for service in services:
		if service[0] in self.__ss_black_list:
			continue
		elif service[1]=="running":
			result.append([service[0],"running"])
		elif service[1]=="dead":
			result.append([service[0],"dead"])
			
	return result

