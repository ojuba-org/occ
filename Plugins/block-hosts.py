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

from gi.repository import Gtk
import re
import urlgrabber.grabber
from OjubaControlCenter.utils import *
from OjubaControlCenter.pluginsClass import PluginsClass
from OjubaControlCenter.utils import run_in_bg
from OjubaControlCenter.widgets import LaunchFileButton, sure, info, error

## NOTE: these global vars is loader validators
category = 'net'
caption = _('Site Blocking')
description = ''
priority = 50

comments_re=re.compile('#.*$',re.M)

def parse_blocked_hosts(h, is_hosts=True):
    """
    return a sorted list of hosts.
    if is_hosts=True then the input is a valid hosts file not a just list of hosts
    """
    if is_hosts: leading=1
    else: leading=0
    h=comments_re.sub('',h)
    l=map(lambda i: i.strip().split(), h.splitlines())
    l=filter(lambda i: len(i)>leading, l)
    l=map(lambda i: i[leading:], l)
    r=sum(l,[])
    r.sort()
    r=uniq(r)
    return r


def get_blocked_hosts_list():
    ua="Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.1) Gecko/20090717 Fedora/3.5.1-1.fc11 Firefox/3.5.1"
    g=urlgrabber.grabber.URLGrabber(user_agent=ua)
    try: l=g.urlread('http://ojuba.org/.blocked_hosts_list.txt')
    except urlgrabber.grabber.URLGrabError:
        return None
    l=map(lambda i: i.strip().split('\t'), l.splitlines())
    l=filter(lambda i: len(i)==4,l)
    return l

def get_blocked_hosts():
    r=[]
    l=get_blocked_hosts_list()
    if not l: return 0,[]
    e=0
    for t,tags,ua,url in l:
        g=urlgrabber.grabber.URLGrabber(user_agent=ua)
        try: h=g.urlread(url)
        except urlgrabber.grabber.URLGrabError: e+=1; continue
        r.extend(parse_blocked_hosts(h, t=='h'))
    # make the list uniq
    r.sort()
    r=uniq(r)
    return e,r

def list_to_hosts(l):
    return "\n".join(map(lambda i: "127.0.0.1\t"+i,l))

class occPlugin(PluginsClass):
    __local_ls_f='/etc/occ/blocked_hosts_local'
    __blocked_ls_f='/etc/occ/blocked_hosts'
    __blocked_f='/etc/occ/enable_blocked_hosts'
    __blacklist_f='/etc/occ/enable_blacklist'
    def __init__(self,ccw):
        PluginsClass.__init__(self, ccw, caption, category, priority)
        self.__lock=True
        vb=Gtk.VBox(False,2)
        self.add(vb)
        hb=Gtk.HBox(False,0); vb.pack_start(hb,False,False,0)
        b=Gtk.Button(_('Filter sites with explicit contents'))
        b.connect('clicked', lambda b: run_in_bg('xdg-open https://addons.mozilla.org/en-US/firefox/addon/1803'))
        hb.pack_start(b,False,False,0)

        hb=Gtk.HBox(False,0); vb.pack_start(hb,False,False,0)
        b=Gtk.CheckButton(_('Block ads and spyware sites'))
        b.set_active(os.path.exists(self.__blocked_f))
        b.connect('toggled', self.__block_cb)
        hb.pack_start(b,False,False,0)
        hb.pack_start(LaunchFileButton(_('View blocked sites list'),self.__blocked_ls_f),False,False,0)
        b=Gtk.Button(stock=Gtk.STOCK_REFRESH)
        b.connect('clicked', self.__refresh_cb)
        b.set_tooltip_text(_('connect to ojuba.org to get the updated list'))
        hb.pack_start(b,False,False,0)
        hb=Gtk.HBox(False,0)
        vb.pack_start(hb,False,False,0)
        b=Gtk.CheckButton(_('Block sites in your personal black list'))
        b.set_active(os.path.exists(self.__blacklist_f))
        b.connect('toggled', self.__personal_list_cb)
        hb.pack_start(b,False,False,0)
        hb=Gtk.HBox(False,0)
        vb.pack_start(hb,False,False,0)
        self.__p=p=Gtk.TextView()
        s=Gtk.ScrolledWindow()
        evb=Gtk.VBox(False,0)
        evb.pack_start(Gtk.Label("Edit your list of banned sites (delimited by spaces and newlines, no commas)"),False,False,0)
        e=Gtk.Expander()
        e.set_label(_("Personal black list"))
        hb.pack_start(e,True,True,6)
        
        e.add(evb)
        evb.pack_start(s,False,False,6)
        s.add(p)
        hb=Gtk.HBox(False,0)
        evb.pack_start(hb,False,False,0)
        b=Gtk.Button(stock=Gtk.STOCK_SAVE)
        b.connect('clicked', self.__save_personal_list_cb)
        hb.pack_start(b,False,False,0)
        self.__load__personal_list()
        self.__lock=False

    def __refresh_cb(self, b):
        e,l=get_blocked_hosts()
        if len(l)<1: error(_("Unable to fetch black list."), self.ccw); return
        r=self.ccw.mechanism('hosts','set_blocked_list', *l)
        if r == 'NotAuth': return
        info(_('Done. You may need to restart your browser.'), self.ccw);
    
    def __load__personal_list(self):
        try: l=open(self.__local_ls_f,"rt").read().strip().split()
        except IOError: return
        l=filter(lambda j: j, map(lambda i: i.strip(), l))
        if not l: return
        self.__p.get_buffer().set_text('\n'.join(l))

    def __save_personal_list_cb(self, b):
        buf=self.__p.get_buffer()
        l=buf.get_text(buf.get_start_iter(),buf.get_end_iter()).strip().split()
        l=filter(lambda j: j, map(lambda i: i.strip(), l))
        self.ccw.mechanism('hosts','set_personal_list', *l)
        info(_('Done. You may need to restart your browser.'), self.ccw);
        #if len(l)<1: error("You list is empty."); return

    def __block_cb(self, b):
        if self.__lock: return
        self.__lock=True
        if b.get_active() and not os.path.exists(self.__blocked_ls_f):
            e,l=get_blocked_hosts()
            r=self.ccw.mechanism('hosts','set_blocked_list', *l)
            if r == 'NotAuth': return
        v=str(int(b.get_active()))
        r=self.ccw.mechanism('hosts','enable_blocked', v)
        if r == 'NotAuth': return
        b.set_active(os.path.exists(self.__blocked_f))
        self.__lock=False
        info(_('Done. You may need to restart your browser.'), self.ccw)

    def __personal_list_cb(self, b):
        if self.__lock: return
        self.__lock=True
        v=str(int(b.get_active()))
        r=self.ccw.mechanism('hosts','enable_black_list', v)
        if r == 'NotAuth': return
        b.set_active(os.path.exists(self.__blacklist_f))
        self.__lock=False
        info(_('Done. You may need to restart your browser.'), self.ccw)



# the following file contains ; as comment
# l    spam    Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.1) Gecko/20090717 Fedora/3.5.1-1.fc11 Firefox/3.5.1    http://www.joewein.de/sw/blacklist/dom-bl.txt

