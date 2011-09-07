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
import re
import os
import os.path
from OjubaControlCenter.mechanismClass import mechanismClass
class OccMechanism(mechanismClass):
  pa_conf='/etc/pulse/default.pa'
  pa_daemon_conf='/etc/pulse/daemon.conf'
  tsched0=re.compile(r"^\s*(load-module module-hal-detect.*?)(\s*\btsched\s*=\s*\S+\b)(.*?)$", re.M)
  tsched=re.compile(r"^\s*(load-module module-hal-detect.*)$", re.M)
  rt_re=re.compile('^(\s*realtime-scheduling\s*=\s*).*\s*$', re.M)
  rt_f_re=re.compile('^(\s*default-fragment-size-msec\s*=\s*).*\s*$', re.M)
  hda_verb_re=re.compile(r'^\s*hda-verb\b.*$',re.M)
  def __init__(self):
    mechanismClass.__init__(self,'snd')

  def hda_verb(self,args):
    if not os.path.exists('/usr/sbin/hda-verb'): return '-1'
    return str(os.system("hda-verb %s" % args))

  def add_hda_verb(self,args):
    if not os.path.exists('/usr/sbin/hda-verb'): return '-1'
    cmd="\nhda-verb %s & # added by OjubaControlCenter\n" % args
    open('/etc/rc.local','at+').write(cmd)
    return '0'

  def remove_hda_verb(self):
    l=open('/etc/rc.local','rt').read()
    l=self.hda_verb_re.sub('',l)
    open('/etc/rc.local','wt').write(l)
    return '0'

  def disable_tsched(self):
    t=open(self.pa_conf,'rt').read()
    t=self.tsched0.sub(r'\1\3',t)
    t=self.tsched.sub(r'\1 tsched=0',t)
    open(self.pa_conf,'wt+').write(t)
    return '0'

  def enable_tsched(self):
    self.reset_rt()
    t=open(self.pa_conf,'rt').read()
    t=self.tsched0.sub(r'\1\3',t)
    open(self.pa_conf,'wt+').write(t)
    return '0'

  def enable_rt(self):
    self.disable_tsched()
    t=open(self.pa_daemon_conf,'rt').read()
    t=self.rt_re.sub('',t)
    t=self.rt_f_re.sub('',t)
    t+="""\nrealtime-scheduling = yes\ndefault-fragment-size-msec = 10\n"""
    open(self.pa_daemon_conf,'wt+').write(t)
    return '0'

  def reset_rt(self):
    t=open(self.pa_daemon_conf,'rt').read()
    t=self.rt_re.sub('',t)
    t=self.rt_f_re.sub('',t)
    open(self.pa_daemon_conf,'wt+').write(t)
    return '0'

