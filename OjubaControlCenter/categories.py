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
# each element is category_id, category_caption, icon_id, category_tip
ls=( \
  ('desktop', _('Desktop'), 'desktop',_('generic desktop preferences and customization')),
  ('gnome', _('GNOME Desktop'), 'gnome-main-menu',_('GNOME desktop preferences and customization')),
  ('install', _('Installer'), 'system-software-install',_('Install applications or setup ojuba')),
  ('hw', _('Hardware'), 'utilities-system-monitor',_('Configure hardware')),
  ('net', _('Network'), 'gtk-network',_('Network related options and settings')),
  ('boot', _('Boot and Kernel'), 'gtk-convert',_('Boot and Kernel')),
  )
#  ('apps', _('Applications'), 'applications-other',_('Launch, install or configure Applications')),
h=dict((i[0],i) for i in ls)
