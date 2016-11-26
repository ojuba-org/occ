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
from OjubaControlCenter.widgets import  sure,info,error


## NOTE: these global vars is loader validators
category = "hw"
caption = _("Power Save")
description = _("Power Save")
priority = 100



class occPlugin(PluginsClass):
    def __init__(self,ccw):
        PluginsClass.__init__(self, ccw, caption, category, priority)



	if self.__check_if_bat() :
		if self.__check_if_tlp("/usr/lib/systemd/system/tlp.service"):

			c=self.__backup_config_file()
			if not c:
				return
			self.notebook=Gtk.Notebook()
			self.add(self.notebook)

			self.page1=Gtk.HBox()
			self.page1.set_border_width(10)
			self.label1=Gtk.Label(_("Service"))
			self.notebook.append_page(self.page1,self.label1)


			self.page2=Gtk.HBox()
			self.page2.set_border_width(10)
			self.label2=Gtk.Label(_("Advanced Configuration"))
			self.notebook.append_page(self.page2,self.label2)

			self.vbox=Gtk.VBox()
			self.page1.pack_start(self.vbox,True,True,0)
			self.hbox1=Gtk.HBox(spacing=20)
			self.vbox.pack_start(self.hbox1,True,True,0)
			
			self.vb1=Gtk.VBox(spacing=3)
			self.vb2=Gtk.VBox(spacing=3)
			self.vb3=Gtk.VBox()
			self.hbox1.pack_start(self.vb1,True,True,0)
			self.hbox1.pack_start(self.vb2,True,True,0)
			self.hbox1.pack_start(self.vb3,True,True,0)

			self.service_label=Gtk.Label(_("<b>Service Name</b>"),use_markup=True)
			self.enabled_status_label=Gtk.Label(_("<b>Enable/Disable</b>"),use_markup=True)
			self.active_status_label=Gtk.Label(_("<b>Start/Stop</b>"),use_markup=True)


			self.grid1=Gtk.Grid(row_homogeneous=True,row_spacing=5)
			self.grid2=Gtk.Grid(row_homogeneous=True)
			self.grid3=Gtk.Grid(row_homogeneous=True)
			self.vb1.pack_start(self.grid1,False,False,0)
			self.vb2.pack_start(self.grid2,False,False,0)
			self.vb3.pack_start(self.grid3,False,False,0)
			self.grid1.attach(self.service_label,0,0,1,1)
			self.grid2.attach(self.enabled_status_label,0,0,1,1)
			self.grid3.attach(self.active_status_label,0,0,1,1)

			self.tlp_name_label=Gtk.Label("TLP")
			if self.__is_enabled_disable("tlp.service"):
				self.enable_disable_tlp_switch=Gtk.Switch()
				self.enable_disable_tlp_switch.set_active(True)
			else:
				self.enable_disable_tlp_switch=Gtk.Switch()
		
			if self.__is_active_dead("tlp.service"):
				self.start_stop_tlp_switch=Gtk.Switch()
				self.start_stop_tlp_switch.set_active(True)
			else:
				self.start_stop_tlp_switch=Gtk.Switch()

			self.enable_disable_tlp_switch.connect("state-set",self.__enable_or_disable,"tlp.service")
			self.start_stop_tlp_switch.connect("state-set",self.__start_or_stop,"tlp.service")
			
			self.grid1.attach(self.tlp_name_label,0,1,1,1)
			self.grid2.attach(self.enable_disable_tlp_switch,0,1,1,1)
			self.grid3.attach(self.start_stop_tlp_switch,0,1,1,1)

			self.tlp_sleep_name_label=Gtk.Label("TLP SLEEP")
			if self.__is_enabled_disable("tlp-sleep.service"):
				self.enable_disable_tlp_sleep_switch=Gtk.Switch()
				self.enable_disable_tlp_sleep_switch.set_active(True)
			else:
				self.enable_disable_tlp_sleep_switch=Gtk.Switch()

			self.enable_disable_tlp_sleep_switch.connect("state-set",self.__enable_or_disable,"tlp-sleep.service")
			self.grid1.attach(self.tlp_sleep_name_label,0,2,1,1)
			self.grid2.attach(self.enable_disable_tlp_sleep_switch,0,2,1,1)





			################################################################
			self.config=self.__get_tlp_config()
			self.vbox2=Gtk.VBox(spacing=20)
			self.page2.pack_start(self.vbox2,True,True,0)		
			self.hbox2=Gtk.HBox(spacing=20)
			self.vbox2.pack_start(self.hbox2,True,True,0)
		
		
			self.vb4=Gtk.VBox(spacing=20)
			self.vb5=Gtk.VBox(spacing=20)
			self.vb6=Gtk.VBox(spacing=20)
			self.hbox2.pack_start(self.vb4,True,True,0)
			self.hbox2.pack_start(self.vb5,True,True,0)
			self.hbox2.pack_start(self.vb6,True,True,0)

			self.config_label=Gtk.Label("<b>Keys</b>",use_markup=True)
			self.config_none=Gtk.Label("")
			self.value_label=Gtk.Label("<b>Values</b>",use_markup=True)
			self.vb4.pack_start(self.config_label,True,True,0)
			self.vb5.pack_start(self.config_none,True,True,0)
			self.vb6.pack_start(self.value_label,True,True,0)

			for k,v in self.config.items():
				self.key_entry=Gtk.Entry(text=v[0],max_length=50)
				self.key_entry.connect('changed', self.__on_key_changed,[k,v])
				self.vb4.pack_start(self.key_entry,True,True,0)
				self.label=Gtk.Label("=")
				self.vb5.pack_start(self.label,True,True,0)
				self.value_entry=Gtk.Entry(text=v[1],max_length=50)
				self.value_entry.connect('changed', self.__on_value_changed,[k,v])
				self.vb6.pack_start(self.value_entry,True,True,0)


			#########################################################################
			self.hbox3=Gtk.HBox()
			self.vbox2.pack_start(self.hbox3,True,True,0)
			self.apply_button=Gtk.Button(label="Apply")
			self.apply_button.connect("clicked",self.__on_button_clicked)
			self.hbox3.pack_start(self.apply_button,True,True,0)
			#########################################################################
			if os.path.isfile("/etc/default/tlp.backup_by_ojuba_occ"):
				self.hbox4=Gtk.HBox()
				self.vbox2.pack_start(self.hbox4,True,True,0)
				self.restore_button=Gtk.Button("Restore Default Config File")
				self.restore_button.connect("clicked",self.__restore_default_file_config)
				self.hbox4.pack_start(self.restore_button,True,True,0)
	

		else:
			self.hbox=Gtk.HBox()
			self.add(self.hbox)
			self.label=Gtk.Label("No TLP Service Detected")
			self.hbox.pack_start(self.label,True,True,0)

	else:
		self.hbox=Gtk.HBox()
		self.add(self.hbox)
		self.label=Gtk.Label("NO Battery Is Detected")
		self.hbox.pack_start(self.label,True,True,0)





    def __on_button_clicked(self,button):
        if not sure(_("Are you sure you want to continue?"), self.ccw):
            return
	count=0
	for l in self.config.values():
		if count==0:
			subprocess.call("echo \'%s=%s\' >/tmp/ojuba_tlp_plugin"%(l[0],l[1]),shell=True)
			count=1
		else:
			subprocess.call("echo \'%s=%s\' >>/tmp/ojuba_tlp_plugin"%(l[0],l[1]),shell=True)
	check=self.ccw.mechanism('run','system',"cat /tmp/ojuba_tlp_plugin >/etc/default/tlp")
	if check!='0':
		return
	self.ccw.mechanism('run','system',"tlp start")
	info(_("Done"))
		
			



		
    def __check_if_bat(self):
	power_supply="/sys/class/power_supply"
	if os.path.isdir(power_supply):
		ls=os.listdir(power_supply)
		if len(ls)!=0:
			for f in ls:
				if f.startswith("BAT"):
					return True
		else:
			return False
	else:
		return False

	return False

    def __check_if_tlp(self,location):
	if os.path.isfile(location):
		return True
	return False

    def __is_active_dead(self,service):
	status= subprocess.Popen("systemctl is-active  %s --no-legend --no-pager --no-ask"%service,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).communicate()[0].decode('utf-8').strip()
	if status=="active":
		return True
	return False

    def __is_enabled_disable(self,service):
	status= subprocess.Popen("systemctl is-enabled %s --no-legend --no-pager --no-ask"%service,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).communicate()[0].decode('utf-8').strip()
	if status=="enabled":
		return True
	return False


    def __enable_or_disable(self,b,s,data):
        if not b.get_state():
            check=self.ccw.mechanism('run','system',"systemctl enable %s"%data)
	    if check!='0':
		error(_("unexpected return code, possible an error had occurred"), self.ccw)
		b.set_state(False)
		b.set_active(False)
		return True

            if not self.__is_enabled_disable(data):
                error(_("unexpected return code, possible an error had occurred"), self.ccw)
                b.set_state(False)
                b.set_active(False)
                return True

	    if data=="tlp.service":
	    	self.ccw.mechanism('run','system',"systemctl mask  systemd-rfkill.service")
                

        else:
            check=self.ccw.mechanism('run','system',"systemctl disable %s"%data)
	    if check!='0':
		error(_("unexpected return code, possible an error had occurred"), self.ccw)
		b.set_state(True)
		b.set_active(True)
		return True
            if self.__is_enabled_disable(data):
                error(_("unexpected return code, possible an error had occurred"), self.ccw)
                b.set_state(True)
                b.set_active(True)
                return True

	    if data=="tlp.service":
	    	self.ccw.mechanism('run','system',"systemctl unmask  systemd-rfkill.service")



    def __start_or_stop(self,b,s,data):
        if not b.get_state():
            check=self.ccw.mechanism('run','system',"systemctl start %s"%data)
	    if check!='0':
		error(_("unexpected return code, possible an error had occurred"), self.ccw)
		b.set_state(False)
		b.set_active(False)
		return True

            if not  self.__is_active_dead(data):
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
            if  self.__is_active_dead(data):
                error(_("unexpected return code, possible an error had occurred"), self.ccw)
                b.set_state(True)
                b.set_active(True)
                return True



    def __on_key_changed(self,entry,data):
	newtext=entry.get_text().strip()
	entry.set_text(newtext)
	self.config[data[0]]=[newtext,self.config[data[0]][1]]
		
    def __on_value_changed(self,entry,data):
	newtext=entry.get_text().strip()
	entry.set_text(newtext)
	self.config[data[0]]=[self.config[data[0]][0],newtext ]

		
    def __get_tlp_config(self):
	result={}
	with open("/etc/default/tlp") as myfile:
		for line in myfile.readlines():
			line=line.strip()
			if len(line)==0 or line.startswith("# "):
				continue
			line=line.split("=")
			result.setdefault(line[0],line)
	return result

    def __backup_config_file(self):
	if not os.path.isfile("/etc/default/tlp.backup_by_ojuba_occ"):
		self.ccw.mechanism('run','system',"cp /etc/default/tlp /etc/default/tlp.backup_by_ojuba_occ")
	if not os.path.isfile("/etc/default/tlp.backup_by_ojuba_occ"):
		return False
	else:
		return True


    def __restore_default_file_config(self,button):
        if not sure(_("Are you sure you want to continue?"), self.ccw):
            return
	check=self.ccw.mechanism('run','system',"cp  /etc/default/tlp.backup_by_ojuba_occ /etc/default/tlp")
	if check!='0':
		return
	info (_("Done"))

