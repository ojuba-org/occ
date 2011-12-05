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

import os
import re
from OjubaControlCenter.utils import *
from OjubaControlCenter.mechanismClass import mechanismClass

class OccMechanism(mechanismClass):
  __local_ls_f='/etc/occ/blocked_hosts_local'
  __blocked_ls_f='/etc/occ/blocked_hosts'
  __blocked_f='/etc/occ/enable_blocked_hosts'
  __blacklist_f='/etc/occ/enable_blacklist'
  __hosts_f='/etc/hosts'
  __blocked_re=re.compile('#@%s START@#(.*)#@%s END@#' % ('system-blocked-list','system-blocked-list'), re.M | re.S)
  __blacklist_re=re.compile('#@%s START@#(.*)#@%s END@#' % ('personal-black-list','personal-black-list'), re.M | re.S)
  def __init__(self):
    mechanismClass.__init__(self,'hosts')
    d=os.path.dirname(self.__local_ls_f)
    if not os.path.exists(d): os.mkdir(d)

  def __list_to_hosts(self, r, comment, l, f):
    s="\n".join(map(lambda i: "127.0.0.1\t"+i.strip(),l))
    ss='''#@%s START@#\n# generated with ojuba control center. don't edit this block.\n%s\n#@%s END@#''' % (comment,s,comment)
    f,n=r.subn(ss,f)
    if n==0: f+="\n"+ss+"\n"
    return f

  def set_blocked_list(self, *l):
    l=list(l)
    try:
      l.extend(map(lambda i: i.strip(), open(self.__blocked_ls_f,"rt+").read().split()))
    except IOError: pass
    l=filter(lambda i: i, l)
    l.sort()
    l=uniq(l)
    f=open(self.__blocked_ls_f,"wt+")
    try: f.write('\n'.join(l))
    except IOError: return '-1'
    f.close()
    return self.gen_hosts()

  def set_personal_list(self, *l):
    l=list(l)
    l.sort()
    l=uniq(l)
    f=open(self.__local_ls_f,"wt+")
    try: f.write('\n'.join(l))
    except IOError: return '-1'
    f.close()
    return self.gen_hosts()

  def enable_blocked(self, v):
    if v!='0':
      try: open(self.__blocked_f,'wt+').close()
      except IOError: return '-1'
    else:
      if os.path.exists(self.__blocked_f): os.unlink(self.__blocked_f)
    return self.gen_hosts()

  def enable_black_list(self, v):
    print v
    if v!='0':
      try: open(self.__blacklist_f,'wt+').close()
      except IOError: return '-1'
    else:
      if os.path.exists(self.__blacklist_f):
        os.unlink(self.__blacklist_f)
        print "unlinked"
    return self.gen_hosts()

  def gen_hosts(self):
    c=open(self.__hosts_f,"rt").read()
    # check if personal black list is enabled
    if os.path.exists(self.__blacklist_f):
      l=map(lambda i: i.strip(), open(self.__local_ls_f,"rt+").read().split())
      l=filter(lambda i: i, l)
      #l.sort()
      #l=uniq(l)
      c=self.__list_to_hosts(self.__blacklist_re, 'personal-black-list', l, c)
    else:
      c=self.__blacklist_re.sub('',c)
    # check if system blocked list is enabled
    if os.path.exists(self.__blocked_f):
      l=map(lambda i: i.strip(), open(self.__blocked_ls_f,"rt+").read().split())
      l=filter(lambda i: i, l)
      #l.sort()
      #l=uniq(l)
      c=self.__list_to_hosts(self.__blocked_re, 'system-blocked-list', l, c)
    else:
      c=self.__blocked_re.sub('',c)
    open(self.__hosts_f,"wt+").write(c)
    return '0'

