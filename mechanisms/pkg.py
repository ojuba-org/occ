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

import re
import os
from glob import glob
from OjubaControlCenter.mechanismClass import mechanismClass

class OccMechanism(mechanismClass):
    name_re=re.compile(r'^\s*name\s*=\s*(.*)\s*$',re.M)
    name_s_re=re.compile(r'^(\s*name\s*=\s*(.*?))\s*$',re.M)
    enabled_re=re.compile(r'^(\s*enabled\s*)=\s*(.*)\s*$',re.M)
    media_re=re.compile(r'^\s*mediaid\s*=\s*(.*)\s*$',re.M)
    keep_cache_re=re.compile(r"^(\s*keepcache)\s*=\s*(.*)\s*$",re.M)
    media_repo_save='/etc/occ/media-repo.save'
    repos_re=re.compile(r"^(\s*\[([^]]+)\][^[]*\s*enabled\s*=\s*)([01])",re.M)
    enabled1_re=re.compile(r"^(\s*enabled\s*=\s*)1(\s*)$",re.M)
    netrepo_re=re.compile(r"^\s*(baseurl|mirrorlist)\s*=\s*(http|https|ftp):",re.M)
    def __init__(self):
        mechanismClass.__init__(self,'pkg')

    def add_media(self, *repos):
        r=0
        for repo in repos:
            try:
                c=open(repo, 'rt').read()
            except IOError: continue
            n=self.name_re.findall(c)
            if not n: continue
            n="mediarepo-"+n[0].replace(' ','-')+".repo"
            c,e=self.enabled_re.subn(r'\1=1',c)
            if e==0: c+="\nenabled=1\n"
            c=self.name_s_re.sub(r'\1 - Media',c)
            try: open(os.path.join('/etc/yum.repos.d',n), 'wt+').write(c)
            except IOError: continue
            r+=1
        return str(r)

    def disable_mediarepo(self):
        r=0
        for repo in glob('/etc/yum.repos.d/*.repo'):
            try:
                c=open(repo, 'rt').read()
            except IOError: continue
            if not self.media_re.search(c): continue
            c,e=self.enabled_re.subn(r'\1=0',c)
            if e==0: c+="\nenabled=0\n"
            try: open(os.path.join('/etc/yum.repos.d',n), 'wt+').write(c)
            except IOError: continue
            r+=1
        return str(r)

    def set_keep_cache(self, v):
        c=open('/etc/yum.conf','rt').read()
        c,n=self.keep_cache_re.subn(r'\1='+v,c)
        if n==0:
            c+="\nkeepcache=%s\n" % v
        open('/etc/yum.conf','wt+').write(c)
        return '0'

    def __get_repos_in_file(self, fn):
        """return tubles repo,is_enabled"""
        c=open(fn,'rt').read()
        return map(lambda a: a[1:],self.repos_re.findall(c))

    def __get_enabled_repos(self):
        """return tuples of (repofile,[repoid1,repoid2]) of enabled repos"""
        repos=[]
        for fn in glob('/etc/yum.repos.d/*.repo'):
            repos.append((fn,map(lambda a:a[0],filter(lambda a:a[1]=='1', self.__get_repos_in_file(fn)))))
        return filter(lambda x: len(x[1])>0, repos)

    def __save_enabled_repos(self):
        if os.path.exists(self.media_repo_save): return
        repos=self.__get_enabled_repos()
        f=open(self.media_repo_save,'wt')
        for i in repos: f.write('%s|%s\n' % (i[0],' '.join(i[1])))
        f.close()


    def __enable_repos_in_file(self, repo):
        """recives a tuple (fn, [repoid,repoid...])"""
        fn=repo[0]
        repoids=repo[1]
        c=open(fn,'rt').read()
        for i in repoids:
            c=re.compile(r"^(\s*\[%s\][^[]*\s*enabled\s*=\s*)([01])" % i,re.M).sub(lambda m: m.expand('\g<1>1'),c)
        open(fn,'wt').write(c)

    def __disable_repo_file(self, fn):
        c=open(fn,'rt').read()
        # replace enabled=1 with 0, ie. perl -i -wpe 's/^(\s*enabled\s*=\s*1)(.*)$/${1}0/' fn
        c,n=self.enabled1_re.subn(r'\g<1>0\2',c)
        if n>0: open(fn,'wt').write(c)
        return n

    def restore_enabled_repos(self):
        if not os.path.exists(self.media_repo_save): return '-1'
        try: l=open(self.media_repo_save,'rt').readlines()
        except IOError: return '-2'
        try: os.unlink(self.media_repo_save)
        except OSError: pass
        count=0
        for i in l:
            a=i.rstrip('\n').split('|')
            if len(a)!=2: continue
            ids=a[1].split(' ')
            self.__enable_repos_in_file((a[0],ids))
            count+=len(ids)
        return str(count)

    def disable_net_repos(self):
        self.__save_enabled_repos()
        count=0
        for fn in glob('/etc/yum.repos.d/*.repo'):
            c=open(fn,'rt').read()
            if self.netrepo_re.search(c):
                cc=self.__disable_repo_file(fn)
                count+=cc
        return str(count)

