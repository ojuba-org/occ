#!/usr/bin/python
# -*- coding: utf-8 -*-

import gobject
import dbus
import dbus.mainloop.glib

import slip.dbus.service

from OCCBackend import Backend

from OjubaControlCenter.odbus import dbus_service_name, dbus_service_path

def run_service ():
  mainloop = gobject.MainLoop ()
  dbus.mainloop.glib.DBusGMainLoop (set_as_default=True)
  system_bus = dbus.SystemBus ()
  name = dbus.service.BusName (dbus_service_name, system_bus)
  backend = Backend (name, dbus_service_path + "/Backend")
  slip.dbus.service.set_mainloop (mainloop)
  mainloop.run ()

if __name__ == "__main__":
  run_service ()
