# -*- coding: utf-8 -*-
"""
Ojuba Control Center
Copyright © 2011, Ojuba.org <core@ojuba.org>

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
import gtk
import os, os.path, shutil
import rpm
from glob import glob
from OjubaControlCenter.widgets import NiceButton, InstallOrInactive, wait, sure, info, error
from OjubaControlCenter.pluginsClass import PluginsClass
from functools  import cmp_to_key

class occPlugin(PluginsClass):
  def __init__(self,ccw):
    self.ts = rpm.TransactionSet()
    self.ts.setVSFlags(rpm._RPMVSF_NOSIGNATURES)
    # will be used to save 450 MB avaliable after copying
    self.LFREE = 450*1024*1024
    
    PluginsClass.__init__(self, ccw,_('Old RPM Files:'),'install',9)
    vb=gtk.VBox(False,2)
    self.add(vb)
    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    l=gtk.Label(_("Ojuba keeps an archive of all the RPM packages downloaded from the internet\nAllowing you to use them when necessary\nHowever, These packages take precious hard disk space.\nYou can save some space by deleting those files.\nYou can also have a backup which you can use later"))
    h.pack_start(l,False,False,2)
    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    self.ccw.rm_old_rpms_b=b=gtk.Button(_('Remove old RPM files'))
    b.connect('clicked', self.rm_rpms_cb)
    h.pack_start(b, False,False,2)
    self.ccw.cp_new_rpms_b=b=gtk.Button(_('Backup new RPM files'))
    b.connect('clicked', self.cp_rpms_cb)
    h.pack_start(b, False,False,2)
  
  def rm_rpms_cb(self, b):
    cmd = '/bin/rm -f'
    dlg=wait()
    dlg.show_all()
    p = self.get_ls()
    if not p:
      dlg.hide()
      info(_("There are no repeated RPM files!"))
      return
    s = self.get_size(p)[1]
    dlg.hide()
    if not sure(_("Delete %d RPM Files, will save %s!\nAre you sure?"%(len(p), s))): return
    cmd = '%s %s'%(cmd, ' '.join(p))
    dlg.show_all()
    try: ret = self.ccw.mechanism('run', 'system', cmd)
    except: ret=0
    dlg.hide()
    if ret: info(_("%d RPM files has been deleted, TO save %s!") %(len(p), s))
    else: info(_("We can't complete this action at this time, due unknown error, you can try again!"))
    
  def cp_rpms_cb(self, b):
    tdir_dlg=sel_dir_dlg()
    if (tdir_dlg.run()==gtk.RESPONSE_ACCEPT):
      tdir = tdir_dlg.get_filename()
      tdir_dlg.hide()
    else:
      tdir_dlg.hide()
      return
    #tdir = '/media/DATA/project/yumarchive/sss'
    dlg=wait()
    dlg.show_all()
    c,r = self.cp(tdir)
    dlg.hide()
    info(_("%d RPM files has been copied\nTo:%s\n%d Repeated RPMS removed!") %(len(c), tdir, len(r))) 
    
  def get_rpms(self, d):
    """find all rpm files """
    r = glob(os.path.join(d, '*.rpm'))
    d2 = filter(lambda i: os.path.isdir(i), map(lambda j: os.path.join(d, j), os.listdir(d)))
    for i in d2:
      r.extend(self.get_rpms(i))
    return r

  def get_ls(self, d='/var/cache/yum',OLD=True):
    self.rpm_list = self.get_rpms(d)
    rpm_ls = self.rpm_list
    rpm_h = {}
    for fn in rpm_ls:
      hdr = self.get_rpm_hdr(fn)
      n = hdr[rpm.RPMTAG_NAME]
      if rpm_h.has_key(n): rpm_h[n].append({"h":hdr, "fn":fn})
      else: rpm_h[n] = [{"h":hdr, "fn":fn}]
    latest_ls = []
    old_ls = []
    for n,l in rpm_h.items():
      latest = max(l, key=cmp_to_key(lambda x,y: rpm.versionCompare(x["h"], y["h"])))
      old = map(lambda a: a['fn'],filter(lambda i: i!=latest, l))
      latest_ls.append(latest['fn'])
      old_ls.extend(old)
    if OLD: return old_ls
    else: return latest_ls
  
  def get_size(self, Files):
    """ return files size """
    m = 0
    for File in Files:
      if os.path.isfile(File):
        m += os.path.getsize(File)
    return m, self.rsize(m)

  def rsize(self, size):
    K = float(1024)
    M = float(1024*1024)
    G = float(1024*1024*1024)
    if size > G: s,m = "GB", float(size/G)
    elif size > M: s,m = "MB", float(size/M)
    elif size > K: s,m = "KB", float(size/K)
    else : s,m = "Bites", size
    r = '%01.02f %s' %(m, s)
    return r

  def get_rpm_hdr(self, fn):
    """ read RPM header """
    ts = self.ts
    fdno = os.open(fn, os.O_RDONLY)
    try: hdr = ts.hdrFromFdno(fdno)
    except: hdr=None ; print 'Error Reading:',fn
    os.close(fdno)
    return hdr
  
  def get_dir_perm(self, d):
    return os.access(d, os.W_OK )

  def get_free_space(self, d):
    stat = os.statvfs(d)
    return stat.f_bsize * stat.f_bavail

  def cp(self, d, OLD=False):
    if not self.get_dir_perm(d): return 0
    files = self.get_ls(OLD=OLD)
    space = self.get_free_space(d)
    size = (self.get_size(files)[0])+self.LFREE
    if size > space: return -1
    copied = []
    for f in files:
      tf = os.path.join(d, os.path.basename(f))
      if not os.path.isfile(tf):
       shutil.copy(f, tf)
       copied.append(tf)
      #os.chown(tf, int(UID), int(GID))
    p = self.get_ls(d)
    removed = []
    if p:
      for f in p:
        os.unlink(f)
        removed.append(f)
    return copied, removed

class sel_dir_dlg(gtk.FileChooserDialog):
  def __init__(self):
    gtk.FileChooserDialog.__init__(self,_("Select directory"), parent=self, buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
    self.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
    self.set_position(gtk.WIN_POS_CENTER)
    self.connect('delete-event', lambda w, *a: w.hide() or True)
    self.connect('response', lambda w, *a: w.hide() or True)


