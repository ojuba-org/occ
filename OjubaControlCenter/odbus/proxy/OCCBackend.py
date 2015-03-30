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

import dbus
#import slip.dbus.polkit as polkit
from OjubaControlCenter.odbus import dbus_service_name, dbus_service_path

class Backend (object):
  def __init__ (self, bus):
    self.bus = bus
    self.dbus_service_path = "/".join ((dbus_service_path, "Backend"))
    self.dbus_object = bus.get_object (dbus_service_name, self.dbus_service_path)
    self.dbus_interface = dbus.Interface (self.dbus_object, dbus_service_name+".Backend")

  #@polkit.enable_proxy
  def call (self,a):
    return self.dbus_interface.call(a)

  #@polkit.enable_proxy
  def Version(self):
    return self.dbus_interface.Version()

