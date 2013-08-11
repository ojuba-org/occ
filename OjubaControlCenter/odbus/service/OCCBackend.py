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

#import glob
#import imputil
#import os
import os.path
import sys
from OjubaControlCenter import loader
from OjubaControlCenter.mechanismClass import mechanismClass
from OjubaControlCenter.odbus import dbus_service_name, dbus_service_path
import dbus.service
import slip.dbus.service
import slip.dbus.polkit as polkit

class Backend (slip.dbus.service.Object):
  default_polkit_auth_required = "org.ojuba.occ.call"
  def __init__ (self, bus_name, object_path):
    slip.dbus.service.Object.__init__ (self, bus_name, object_path)
    print "*** Serivce __init__: Running occ dbus service at '%s'." % (dbus_service_name)
    self.__load()

  def __load(self):
    exeDir=os.path.abspath(os.path.dirname(sys.argv[0]))
    pluginsDir=os.path.join(exeDir,'mechanisms')
    if not os.path.isdir(pluginsDir):
      pluginsDir=os.path.join(exeDir,'..','share','occ','mechanisms')
    l = loader.Loader(pluginsDir,mechanismClass,'OccMechanism')
    p=l.load_mech(pluginsDir,mechanismClass,'OccMechanism')
    self.__m={}
    for i in p: self.__m[i.name]=i
    #print self.__m
    #self.__m['ping'].call('foo','bar')

  @polkit.require_auth("org.ojuba.occ.call")
  #@dbus.service.method(dbus_interface = dbus_service_name + ".Backend", in_signature="", out_signature="")
  @dbus.service.method(dbus_interface = dbus_service_name + ".Backend")
  def call(self,args):
    #print args
    M=args[0]
    a=args[1:]
    if self.__m.has_key(M): r=self.__m[M].call(*a)
    else: r=''
    return r

  @dbus.service.method(dbus_interface = dbus_service_name + ".Backend")
  def Version(self):
    return "0.1"


