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

#import pty
#import signal
#import os
#import time
from gi.repository import Gtk
import re
#from subprocess import *
from glob import glob
from OjubaControlCenter.pluginsClass import PluginsClass
from OjubaControlCenter.widgets import LaunchOrInstall, InstallOrInactive, sure

## NOTE: these global vars is loader validators
category = 'hw'
caption = _('Printer settings and tools')
description = ''
priority = 30

class occPlugin(PluginsClass):
    amixer_re=re.compile("""^\S[^'\n]+'([^'\n]+)'""",re.M)
    def __init__(self,ccw):
        self.__hda_verb_needed=None
        PluginsClass.__init__(self, ccw, caption, category, priority)
        vb=Gtk.VBox(False,2)
        self.add(vb)
        hb=Gtk.HBox(False,2); vb.pack_start(hb,True,True,2)
        b=LaunchOrInstall(self,_('Configure printers'),'/usr/bin/system-config-printer',['system-config-printer'])
        hb.pack_start(b,False,False,2); hb=Gtk.HBox(False,2); vb.pack_start(hb,True,True,2)
        b=InstallOrInactive(self, _("Install support for non-standard printers (GDI or winprinters)"), _("extra packages are already installed"), _("Install foo2* packages"), ["foo2qpdl", "foo2hiperc", "foo2lava", "foo2hp", "foo2slx", "foo2xqx", "foo2zjs"])
        hb.pack_start(b,False,False,2)
#        b=InstallOrInactive(self, "Install HIPERC support","foo2hiperc is already installed",'support for HIPERC printers such as <b>Oki</b> C3100n, C3200n, C3300n, C3400n, C3530n MFP, C5100n, C5150n, C5200n, C5500n, C5600n and C5800n',['foo2hiperc'])
#        hb.pack_start(b,False,False,2); hb=Gtk.HBox(False,2); vb.pack_start(hb,True,True,2)
#        b=InstallOrInactive(self, "Install HP ZjStream support (winprinters)","foo2hp is already installed",'support for ZjStream printers such as HP Color LaserJet CP1215, HP Color LaserJet 1600, HP Color LaserJet 2600n',['foo2hp'])
#        hb.pack_start(b,False,False,2); hb=Gtk.HBox(False,2); vb.pack_start(hb,True,True,2)
#        b=InstallOrInactive(self, "Install QPDL support (winprinters)", "foo2qpdl is already installed",'support for QPDL printers such as:\nSamsung CLP-300, CLP-310, CLP-315, CLP-600, CLP-610, CLX-2160, CLX-3160, CLX-3175\nXerox Phaser 6110 or Xerox Phaser 6110MFP', ['foo2qpdl'])
#        hb.pack_start(b,False,False,2); hb=Gtk.HBox(False,2); vb.pack_start(hb,True,True,2)
#        b=InstallOrInactive(self, "Install OAKT support (winprinters)","foo2oak is already installed",'support for Zoran/OAKT printers such as HP Color LaserJet 1500, Kyocera KM-1635 and the Kyocera KM-2035.',['foo2oak'])
#        hb.pack_start(b,False,False,2); hb=Gtk.HBox(False,2); vb.pack_start(hb,True,True,2)
#        b=InstallOrInactive(self, "Install ZjStream support (winprinters)","foo2zjs is already installed",'support for ZjStream printers such as Minolta/QMS magicolor 2200/2300 DL, Minolta Color PageWorks/Pro L,\n Konica Minolta magicolor 2430 DL,\n HP LaserJet P2035, 1022, 1020, 1018 ,1005, 1000, M1319 MFP.',['foo2zjs'])
#        hb.pack_start(b,False,False,2)
#'foo2lava' 'foo2slx' 'foo2xqx' 'foo2zjs' 
