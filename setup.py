#! /usr/bin/python
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
from distutils.core import setup
from glob import glob

# to install type: 
# python setup.py install --root=/
locales = map(lambda i: ('share/' + i,['' + i + '/occ.mo',]), glob('locale/*/LC_MESSAGES'))
data_files = [
    ('/etc/dbus-1/system.d', ['config/org.Ojuba.OCC.conf']),
    ('share/polkit-1/actions',['config/org.ojuba.occ.policy']),
    ('share/dbus-1/system-services',['config/org.Ojuba.OCC.service']),
    ('share/occ',['occ-mechanism.py']),
    ('share/occ/Plugins', glob('Plugins/*.py') ),
    ('share/occ/mechanisms',glob('mechanisms/*.py')),
    ('share/applications',['occ.desktop']),
    ('share/icons/hicolor/scalable/apps', ['ojuba-control-center.svg']),
    ('bin',['occ','legacy2opentype','RunOrInstall']),
]
data_files.extend(locales)
setup (name = 'occ', version = '2.0.0',
      description = 'Ojuba Control Center',
      author = 'Muayyad Saleh Alsadi',
      author_email = 'alsadi@ojuba.org',
      url = 'http://linux.ojuba.org/',
      license = 'Waqf',
      packages = ['OjubaControlCenter',
                  'OjubaControlCenter.odbus',
                  'OjubaControlCenter.odbus.service',
                  'OjubaControlCenter.odbus.proxy'],
      data_files = data_files
)

