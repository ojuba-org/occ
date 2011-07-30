# -*- coding: utf-8 -*-
"""
Ojuba Control Center
Copyright © 2009, Muayyad Alsadi <alsadi@ojuba.org>

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
import gtk, os

from OjubaControlCenter.pluginsClass import PluginsClass
from OjubaControlCenter.utils import  which_exe
from OjubaControlCenter.widgets import LaunchOrInstall, InstallOrInactive, wait, info, sure, error
#import rpm
#ts = rpm.TransactionSet() 
#for i in ts.dbMatch('name','wine'): print i['name'],i['version'],i['FILENAMES']
#if ts.dbMatch('name','bogus_package',1).count()==0: print not installed

class Separator(gtk.HBox):
  def __init__(self):
    gtk.HBox.__init__(self)
    self.pack_start(gtk.HSeparator(),True,True,150)
    #self.set_property('width-request', 50)
    
class occPlugin(PluginsClass):
  #if (sys.maxsize > 2**32): arch = 'x86_64'
  #else: arch = 'i386'
  basearch=os.uname()[4]
  if basearch=='i686': basearch='i386'
  opera_url="ftp://ftp.opera.com/pub/opera/linux/1150/opera-11.50-1074.%s.rpm"%basearch
  def __init__(self,ccw):
    PluginsClass.__init__(self, ccw,_('Favorite Packages'),'install',20)
    vb=gtk.VBox(False,2)
    self.add(vb)
    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    l=gtk.Label(_('Those are some selected software packages.\nIf you got packages DVD, you may like to enable it before installing the packages.'))
    h.pack_start(l,False,False,2)
    hb=gtk.HBox(False,0); vb.pack_start(hb,False,False,6) 
    hb.pack_start(gtk.Label(_('Desktop:')),False,False,2)
    #hb.pack_start(LaunchOrInstall(self,'Compiz Fusion','/usr/bin/fusion-icon-gtk',['fusion-icon-gtk','compiz-fusion-extras','compiz-fusion-extras-gnome','ccsm','emerald-themes','emerald']),False,False,2)
    hb.pack_end(LaunchOrInstall(self,'Gnome Do','/usr/bin/gnome-do',['gnome-do','gnome-do-plugins', 'gnome-do-plugins-firefox','gnome-do-plugins-thunderbird', 'gnome-do-plugins-eog','gnome-do-plugins-pidgin']),False,False,2)
    hb.pack_end(LaunchOrInstall(self,'Avant Window Navigator','/usr/bin/avant-window-navigator',['avant-window-navigator']),False,False,2)
    hb.pack_end(LaunchOrInstall(self,'cairo dock','/usr/bin/cairo-dock',['cairo-dock','cairo-dock-plug-ins','cairo-dock-plug-ins-webkit']),False,False,2)
    #hb.pack_start(LaunchOrInstall(self,'screenlets','/usr/bin/screenlets',['screenlets']),False,False,2)
    hb.pack_end(InstallOrInactive(self, _('extra screensavers'), _('extra screensavers'), _('extra screensavers'), ['xscreensaver-extras', 'xscreensaver-extras-gss', 'xscreensaver-gl-base', 'xscreensaver-gl-extras' , 'xscreensaver-gl-extras-gss','rss-glx','rss-glx-gnome-screensaver']),False,False,2)

    vb.pack_start(Separator(),False,False,6)
    hb=gtk.HBox(False,0); vb.pack_start(hb,False,False,6)
    hb.pack_start(gtk.Label(_('Internet:')),False,False,2)
    hb.pack_end(LaunchOrInstall(self,'Chromium browser','/usr/bin/chromium-browser',['chromium']),False,False,2)
    b=gtk.Button('Opera browser')
    b.connect('clicked', self.inst_opera)
    b.set_sensitive(not which_exe('opera'))
    hb.pack_end(b,False,False,2)
    
    hb.pack_end(LaunchOrInstall(self,'gyachi Yahoo chat','/usr/bin/gyachi',['gyachi']),False,False,2)
    hb.pack_end(InstallOrInactive(self, 'Skype', 'Skype is installed','a proprietary video chat', ['skype']),False,False,2)

    vb.pack_start(Separator(),False,False,6)
    hb=gtk.HBox(False,0); vb.pack_start(hb,False,False,6)
    hb.pack_start(gtk.Label(_('Mobile related:')),False,False,2)
    hb.pack_end(LaunchOrInstall(self,'wammu PC Suite','/usr/bin/wammu',['wammu']),False,False,2)
    hb.pack_end(LaunchOrInstall(self,'xgnokii','/usr/bin/xgnokii',['xgnokii']),False,False,2)

    vb.pack_start(Separator(),False,False,6)
    hb=gtk.HBox(False,0); vb.pack_start(hb,False,False,6)
    hb.pack_start(gtk.Label(_('Multimedia and Grpahics:')),False,False,2)
    hb.pack_end(LaunchOrInstall(self,'kdenlive video editor','/usr/bin/kdenlive',['kdenlive']),False,False,2)
    hb.pack_end(LaunchOrInstall(self,'avidemux video editor','/usr/bin/avidemux2_qt4',['avidemux-qt']),False,False,2)
    hb.pack_end(LaunchOrInstall(self,'kino video editor','/usr/bin/kino',['kino']),False,False,2)
    hb=gtk.HBox(False,0); vb.pack_start(hb,False,False,6)
    hb.pack_end(LaunchOrInstall(self,'EasyTag','/usr/bin/easytag',['easytag']),False,False,2)
    hb.pack_end(LaunchOrInstall(self,'DeVeDe','/usr/bin/devede',['devede']),False,False,2)
    hb.pack_end(InstallOrInactive(self, 'GIMP Help', 'GIMP Help', 'GIMP Help', ['gimp-help-browser', 'gimp-help']),False,False,2)
    hb.pack_end(LaunchOrInstall(self,'Inkscape','/usr/bin/inkscape',['inkscape']),False,False,2)
    hb.pack_end(LaunchOrInstall(self,'Blender 3D','/usr/bin/blender-freeworld.bin',['blender-freeworld','blenderplayer-freeworld']),False,False,2)
    hb.pack_end(InstallOrInactive(self, 'yafray', 'yafray', 'yafray 3D renderer', ['yafray']),False,False,2)

    vb.pack_start(Separator(),False,False,6)
    hb=gtk.HBox(False,0); vb.pack_start(hb,False,False,6)
    hb.pack_start(gtk.Label(_('Games:')),False,False,2)
    hb.pack_end(LaunchOrInstall(self,'Pingus','/usr/bin/pingus',['pingus']),False,False,2)
    hb.pack_end(LaunchOrInstall(self,'Wormux','/usr/bin/wormux',['wormux']),False,False,2)
    hb.pack_end(LaunchOrInstall(self,_('Secret Maryo Chronicles'),'/usr/bin/smc',['smc']),False,False,2)
    hb.pack_end(LaunchOrInstall(self,'Mega Mario', '/usr/bin/megamario',['megamario']),False,False,2)
    hb.pack_end(LaunchOrInstall(self,'supertux','/usr/bin/supertux',['supertux']),False,False,2)
    hb=gtk.HBox(False,0); vb.pack_start(hb,False,False,6)
    hb.pack_end(LaunchOrInstall(self, 'Rocks n Diamonds','/usr/bin/rocksndiamonds',['rocksndiamonds']),False,False,2)
    hb.pack_end(LaunchOrInstall(self, 'Enigma','/usr/bin/enigma',['enigma']),False,False,2)
    hb.pack_end(LaunchOrInstall(self, 'solarwolf','/usr/bin/solarwolf',['solarwolf']),False,False,2)
    hb.pack_end(LaunchOrInstall(self,'frozen-bubble','/usr/bin/frozen-bubble',['frozen-bubble']),False,False,2)

    hb=gtk.HBox(False,0); vb.pack_start(hb,False,False,6)
    #hb.pack_start(gtk.VBox(False,0),True,True,2)

    hb.pack_end(LaunchOrInstall(self,'War Zone 2100','/usr/bin/warzone2100',['warzone2100']),False,False,2)
    hb.pack_end(LaunchOrInstall(self,'maniadrive','/usr/bin/maniadrive',['maniadrive']),False,False,2)
    hb.pack_end(LaunchOrInstall(self,'supertuxkart','/usr/bin/supertuxkart',['supertuxkart']), False,False,2)
    hb.pack_end(LaunchOrInstall(self, 'extremetuxracer','/usr/bin/extremetuxracer',['extremetuxracer']),False,False,2)
    hb=gtk.HBox(False,0); vb.pack_start(hb,False,False,6)
    hb.pack_end(LaunchOrInstall(self,'xmoto','/usr/bin/xmoto',['xmoto']),False,False,2)
    hb.pack_end(LaunchOrInstall(self,'neverball','/usr/bin/neverball',['neverball']),False,False,2)
    hb.pack_end(LaunchOrInstall(self,'foobillard','/usr/bin/foobillard',['foobillard']),False,False,2)
    hb.pack_end(LaunchOrInstall(self,'armacycles-ad','/usr/bin/armacycles-ad',['armacycles-ad']),False,False,2)

    vb.pack_start(Separator(),False,False,6)
    hb=gtk.HBox(False,0); vb.pack_start(hb,False,False,6)
    hb.pack_start(gtk.Label(_('Development:')),False,False,2)
    hb.pack_end(LaunchOrInstall(self,'Nokia Qt Creator','/usr/bin/qtcreator.bin',['qt-creator']),False,False,2)
    hb.pack_end(LaunchOrInstall(self, 'Qt Designer', '/usr/bin/designer-qt4', ['qt-devel']),False,False,2)
    hb.pack_end(LaunchOrInstall(self,'Gambas BASIC','/usr/bin/gambas2',['gambas2-ide']),False,False,2)
    hb.pack_end(LaunchOrInstall(self,'MonoDevelop for C#','/usr/bin/monodevelop',['monodevelop']),False,False,2)
    hb=gtk.HBox(False,0); vb.pack_start(hb,False,False,6)
    hb.pack_end(LaunchOrInstall(self,'Eclipse IDE', '/usr/bin/eclipse' ,['eclipse-cdt','eclipse-changelog','eclipse-jdt','eclipse-mylyn','eclipse-mylyn-java','eclipse-pde','eclipse-pydev','eclipse-rpm-editor','eclipse-subclipse']),False,False,2)
    hb.pack_end(LaunchOrInstall(self,'Netbeans IDE', '/usr/bin/netbeans', ['netbeans']),False,False,2)

    vb.pack_start(Separator(),False,False,6)
    hb=gtk.HBox(False,0); vb.pack_start(hb,False,False,6)
    hb.pack_start(gtk.Label(_('Servers:')),False,False,2)
    hb.pack_end(InstallOrInactive(self, _('web server collection'), _('web server collection'), _('collection of LAMP web server related packages'), ['httpd', 'crypto-utils', 'distcache', 'httpd-manual', 'mod_perl', 'mod_python', 'mod_wsgi', 'mod_ssl', 'php', 'php-ldap', 'php-mysql', 'squid', 'webalizer', 'system-config-httpd']),False,False,2)
    hb.pack_end(InstallOrInactive(self, _('ftp server'), _('ftp server'), _('collection of ftp server related packages'), ['vsftpd', 'system-config-vsftpd']),False,False,2)
    hb.pack_end(InstallOrInactive(self, _('tomcat collection'), _('tomcat collection'), _('collection of tomcat related packages'), ['tomcat6-webapps','tomcat6-servlet','tomcat6-admin-webapps']),False,False,2)
    hb.pack_end(InstallOrInactive(self, _('Jetty Java Servlet'), _('Jetty Java Servlet'), _('Jetty is a pure Java HTTP Server and Servlet Container'), ['jetty']),False,False,2)
    #hb.pack_start(InstallOrInactive(self, _('clustering collection'), _('clustering collection'), _('collection of clustering related packages'), ['cluster-cim', 'cluster-snmp', 'ipvsadm', 'modcluster', 'rgmanager', 'ricci', 'system-config-cluster']),False,False,2)

    vb.pack_start(Separator(),False,False,6)
    hb=gtk.HBox(False,0); vb.pack_start(hb,False,False,6)
    hb.pack_start(gtk.Label(_('Engineering:')),False,False,2)
    hb.pack_end(LaunchOrInstall(self,'wxMaxima CAS','/usr/bin/wxmaxima',['wxMaxima']),False,False,2)
    hb.pack_end(LaunchOrInstall(self,'Qt Octave','/usr/bin/qtoctave',['qtoctave']),False,False,2)
    hb.pack_end(LaunchOrInstall(self,'qcad','/usr/bin/qcad',['qcad']),False,False,2)
    hb.pack_end(InstallOrInactive(self, _('Circuits collection'), _('Circuits collection already installed'), _('Circuits collection'), ['kicad', 'gspiceui', 'gnucap', 'gwave', 'ngspice', 'geda-gschem', 'electronics-menu','qucs']),False,False,2)
    hb.pack_end(LaunchOrInstall(self,'K Stars','/usr/bin/kstars',['kdeedu-kstars']),False,False,2)

  def inst_opera(self, b):
    print self.opera_url
    if which_exe('opera'): info(_('already installed')); return
    dlg=wait()
    r=self.ccw.mechanism('run','system','rpm -Uvh "%s"' % self.opera_url, on_fail='-1')
    dlg.hide()
    if dlg: dlg.destroy()
    if r!='0': error(_("unexpected return code, possible an error had occurred."))

