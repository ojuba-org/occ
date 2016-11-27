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
from OjubaControlCenter.widgets import  sure,info,wait,InstallOrInactive


## NOTE: these global vars is loader validators
category = "boot"
caption = _("Boot Loader Manager")
description = _("Grub Manager")
priority = 100



class occPlugin(PluginsClass):
    def __init__(self,ccw):
        PluginsClass.__init__(self, ccw, caption, category, priority)

	c=self.__backup_config_file()
	if not c:
		return
	self.notebook=Gtk.Notebook()
	self.add(self.notebook)
	
	self.page1=Gtk.HBox()
	self.page1.set_border_width(10)
	self.label1=Gtk.Label(_("Grub Config"))
	self.notebook.append_page(self.page1,self.label1)

	self.page2=Gtk.HBox()
	self.page2.set_border_width(10)
	self.label2=Gtk.Label(_("Refresh Boot Loader"))
	self.notebook.append_page(self.page2,self.label2)

	self.__to_order_d=[]
	self.config=self.__get_grub_config()

	self.vbox1=Gtk.VBox(spacing=20)
	self.page1.pack_start(self.vbox1,True,True,0)		
	self.hbox1=Gtk.HBox(spacing=20)
	self.vbox1.pack_start(self.hbox1,True,True,0)
		
		
	self.vb1=Gtk.VBox(spacing=20)
	self.vb2=Gtk.VBox(spacing=20)
	self.vb3=Gtk.VBox(spacing=20)
	self.hbox1.pack_start(self.vb1,True,True,0)
	self.hbox1.pack_start(self.vb2,True,True,0)
	self.hbox1.pack_start(self.vb3,True,True,0)

	self.config_label=Gtk.Label("<b>Keys</b>",use_markup=True)
	self.config_none=Gtk.Label("")
	self.value_label=Gtk.Label("<b>Values</b>",use_markup=True)
	self.vb1.pack_start(self.config_label,True,True,0)
	self.vb2.pack_start(self.config_none,True,True,0)
	self.vb3.pack_start(self.value_label,True,True,0)

	for n in self.__to_order_d:
		self.key_entry=Gtk.Entry(text=self.config[n][0],max_length=100)
		self.key_entry.connect('changed', self.__on_key_changed,[n,self.config[n]])
		self.vb1.pack_start(self.key_entry,True,True,0)
		self.label=Gtk.Label("=")
		self.vb2.pack_start(self.label,True,True,0)
		self.value_entry=Gtk.Entry(text=self.config[n][1],max_length=300)
		self.value_entry.connect('changed', self.__on_value_changed,[n,self.config[n]])
		self.vb3.pack_start(self.value_entry,True,True,0)



	self.hbox3=Gtk.HBox()
	self.vbox1.pack_start(self.hbox3,True,True,0)
	self.apply_button=Gtk.Button(label="Apply")
	self.apply_button.connect("clicked",self.__on_button_clicked)
	self.hbox3.pack_start(self.apply_button,True,True,0)

	if os.path.isfile("/etc/default/grub.backup_by_ojuba_occ"):
		self.hbox4=Gtk.HBox()
		self.vbox1.pack_start(self.hbox4,False,False,0)
		self.restore_button=Gtk.Button("Restore Default Config File")
		self.restore_button.connect("clicked",self.__restore_default_file_config)
		self.hbox4.pack_start(self.restore_button,True,True,0)
	

	self.vbox2=Gtk.VBox(spacing=10)
	self.page2.pack_start(self.vbox2,True,True,0)

	#from os-prob.py plugin
        m=InstallOrInactive(self, _("Install os prober"),_("os prober is installed"), _('package detects other OSes available on a system'), ['os-prober'])
	self.vbox2.pack_start(m,False,False,0)

        self.apply_b = b = Gtk.Button(_('Find and add installed systems to grub menu'))
        b.set_sensitive(not m.get_sensitive())
        b.connect('clicked', self.apply_cb)
	self.vbox2.pack_start(b,False,False,0)


    def __on_button_clicked(self,button):
        if not sure(_("Are you sure you want to continue?"), self.ccw):
            return

	count=0
	for n in self.__to_order_d:
		if count==0:
			subprocess.call(r"echo '%s=%s' >/tmp/ojuba_grub_plugin"%(self.config[n][0],self.config[n][1]),shell=True)
			count=1
		else:
			subprocess.call(r"echo '%s=%s' >>/tmp/ojuba_grub_plugin"%(self.config[n][0],self.config[n][1]),shell=True)
	check=self.ccw.mechanism('run','system',"cp /tmp/ojuba_grub_plugin /etc/default/grub")
	if check!='0':
		return info(_("Change Config Fail"))

	check=self.__update_grub()
	if not check:
		return info(_("Update Grub Menu Fail Restore Default Config File And Restart occ"))

	info(_("Done"))


    def __update_grub(self):
	if os.path.isdir("/sys/firmware/efi/efivars"):
		check=self.ccw.mechanism('run','system',"grub2-mkconfig -o /boot/efi/EFI/fedora/grub.cfg")
		if check!='0':
			return False
	else:
		check=self.ccw.mechanism('run','system',"grub2-mkconfig -o /boot/grub2/grub.cfg")
		if check!='0':
			return False
	return True
	




    def __on_key_changed(self,entry,data):
	newtext=entry.get_text().strip()
	entry.set_text(newtext)
	self.config[data[0]]=[newtext,self.config[data[0]][1]]
		
    def __on_value_changed(self,entry,data):
	newtext=entry.get_text().strip()
	entry.set_text(newtext)
	self.config[data[0]]=[self.config[data[0]][0],newtext ]

	


    def __get_grub_config(self):
	result={}
	with open("/etc/default/grub") as myfile:
		for line in myfile.readlines():
			line=line.strip()
			if len(line)==0:
				continue
			line=line.split("=",1)
			if line[0].startswith("GRUB_DISTRIBUTOR"):
				result.setdefault(line[0],[line[0],"""\"$(sed '"'"'s, release .*$,,g'"'"' /etc/system-release)\""""])

				self.__to_order_d.append(line[0])
			else:
				result.setdefault(line[0],line)
				self.__to_order_d.append(line[0])

	return result



    def __backup_config_file(self):
	if not os.path.isfile("/etc/default/grub.backup_by_ojuba_occ"):
		self.ccw.mechanism('run','system',"cp /etc/default/grub /etc/default/grub.backup_by_ojuba_occ")
	if  not os.path.isfile("/etc/default/grub.backup_by_ojuba_occ"):
		return False
	else:
		return True



    def __restore_default_file_config(self,button):
        if not sure(_("Are you sure you want to continue?"), self.ccw):
            return
	check=self.ccw.mechanism('run','system',"cp  /etc/default/grub.backup_by_ojuba_occ /etc/default/grub")
	if check!='0':
		return info (_("Restore Default Config File Fail"))
	check=self.__update_grub()
	if not check:
		return info(_("Update Grub Menu Fail"))

	info (_("Done"))

     #from os-prob.py plugin
    def apply_cb(self, w):
        if not sure(_('Are you sure you want to detect and add other operating systems?'), self.ccw): return
        dlg=wait(self.ccw)
        dlg.show_all()
        r=self.ccw.mechanism('grub2','os_prober_cb')
        dlg.hide()
        if r == 'NotAuth': return 
        if r.startswith("Error"): return info('%s: %s'%(_('Error'),r[6:]))
        info(_('Operating systems found:\n%s') % r,self.ccw)
