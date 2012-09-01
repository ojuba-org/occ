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

import os
import re
from glob import glob
from itertools import groupby
from subprocess import Popen, PIPE

setsid = getattr(os, 'setsid', None)
if not setsid: setsid = getattr(os, 'setpgrp', None)
_ps=[]

def chkconfig(runlevel, service):
    l=glob('/etc/rc%i.d/S[0-9][0-9]%s' % (runlevel, service))
    if len(l)<1: return False
    p=l[0]
    return (os.stat(p)[0]&0100)!=0
#    # old method
#    s=Popen(["chkconfig", "--list", service], stdout=PIPE).communicate()[0]
#    if not s: return False
#    try: return s.strip().split('\t')[runlevel+1].split(':')[1].lower()=='on'
#    except IndexError: return False
        
def uniq(l):
    return map(lambda g: g[0], groupby(l))

def run_in_bg(cmd):
    global _ps
    setsid = getattr(os, 'setsid', None)
    if not setsid: setsid = getattr(os, 'setpgrp', None)
    _ps=filter(lambda x: x.poll()!=None,_ps) # remove terminated processes from _ps list
    _ps.append(Popen(cmd,0,'/bin/sh',shell=True, preexec_fn=setsid))

def get_pids(l):
    pids=[]
    for i in l:
        p=Popen(['/sbin/pidof',i], 0, stdout=PIPE)
        l=p.communicate()[0].strip().split()
        r=p.returncode
        if r==0: pids.extend(l)
    pids.sort()
    return pids

def get_desktop():
    """return 1 for kde, 0 for gnome, -1 none of them"""
    l=get_pids(('kwin','ksmserver',))
    if l: kde=l[0]
    else: kde=None
    l=get_pids(('gnome-session',))
    if l: gnome=l[0]
    else: gnome=None
    if kde:
        if not gnome or kde<gnome: return 1
        else: return 0
    if gnome: return 0
    else: return -1

def file_man_cmd(mp):
    if get_desktop()==0: return 'nautilus --no-desktop "%s"' % mp
    elif get_desktop()==1: return 'konqueror "%s"' % mp
    elif os.path.exists('/usr/bin/thunar'): return 'thunar "%s"' % mp
    elif os.path.exists('/usr/bin/pcmanfm'): return 'pcmanfm "%s"' % mp
    elif os.path.exists('/usr/bin/nautilus'): return 'nautilus --no-desktop "%s"' % mp
    elif os.path.exists('/usr/bin/konqueror'): return 'konqueror "%s"' % mp
    return None

def run_file_man(mp): run_in_bg(file_man_cmd(mp))

def which_exe(bin_fn):
    for i in os.environ['PATH'].split(':'):
        p=os.path.join(i,bin_fn)
        if os.path.exists(p) and os.stat(p).st_mode & 1: return p
    return None

_ch_re=re.compile(r'\\(0\d\d)')

def decode_mounts(s):
    return _ch_re.sub(lambda m: chr(int(m.group(1),8)), s)

def get_mounts(unique=True, mnt_filter=None, dev_filter=None):
    by_mnt={}
    by_dev={}
    for i in open('/proc/mounts','rt'):
        p=decode_mounts(i.split()[1].strip())
        d=decode_mounts(i.split()[0].strip())
        if unique and by_dev.has_key(d): continue
        if dev_filter and not dev_filter(d): continue
        if mnt_filter and not mnt_filter(p): continue
        by_mnt[p]=d
        by_dev[d]=p
    return by_mnt, by_dev

def cmd_out(cmd):
    out, err = Popen(cmd , shell=True, stdout=PIPE, stderr=PIPE).communicate()
    return (out.strip(), err.strip())
    
def copyfile(source, dest, buffer_size=1024*1024):
    """
    Copy a file from source to dest. source and dest
    can either be strings or any object with a read or
    write method, like StringIO for example.
    """
    if not hasattr(source, 'read'):
        source = open(source, 'rb')
    if not hasattr(dest, 'write'):
        dest = open(dest, 'wb')
    while 1:
        copy_buffer = source.read(buffer_size)
        if copy_buffer:
            dest.write(copy_buffer)
        else:
            break
    source.close()
    dest.close()
    return True
