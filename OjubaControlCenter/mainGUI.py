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

import os, sys
import gettext

ld=os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])),'..','share','locale')
if not os.path.exists(ld): ld=os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])),'locale')
gettext.install('occ', ld, unicode=0)


from gi.repository import Gtk

from OjubaControlCenter import loader
from OjubaControlCenter import categories
from OjubaControlCenter.pluginsClass import PluginsClass
from OjubaControlCenter.widgets import error, LaunchButton, CatFrame, MainButton, getSpecialIcon


class GUI(Gtk.VBox):
        def __init__(self, ccw):
                Gtk.VBox.__init__(self, False, 2)
                self.ccw = ccw
                self.vis_plugins = []
                self.cat_v={}
                self.cat_c={}
                self.cat_plugins={}
                self.cat_buttons={}
                skip = sum(map(lambda a: a[15:].split(','),
                                                filter(lambda s: s.startswith('--skip-plugins='),
                                                            sys.argv[1:])),[])
                debug = '--debug' in sys.argv[1:]
                self.__exeDir=os.path.abspath(os.path.dirname(sys.argv[0]))
                self.__pluginsDir=os.path.join(self.__exeDir,'Plugins')
                if not os.path.isdir(self.__pluginsDir):
                        self.__pluginsDir=os.path.join(self.__exeDir,'..','share','occ','Plugins')
                self.Loader = loader.Loader(self.__pluginsDir,
                                                                        PluginsClass,
                                                                        'occPlugin',
                                                                        skip,
                                                                        debug,
                                                                        self.ccw)
                
                h=Gtk.HBox(False,6)
                self.pack_start(h,False,False,6)
                l=Gtk.Label()
                l.set_markup("""<span size="xx-large"><b>:::</b></span>""")

                self.GoMain_b = b = Gtk.Button()
                b.set_tooltip_markup("""<span size="large">%s</span>""" % (_("Back to Main")))
                b.add(l)
                b.set_focus_on_click(False)
                b.connect('clicked', self.show_main_cb)
                h.pack_start(b,False,False,6)

                b=Gtk.Button()
                b.add(Gtk.Image.new_from_icon_name('ojuba-control-center',Gtk.IconSize.DIALOG))
                b.set_tooltip_markup("""<span size="large">%s</span>""" % (_("About Ojuba Control Center")))
                b.set_focus_on_click(False)
                b.connect('clicked', self.show_about_dlg)
                h.pack_end(b, False, False, 6)

                self.searh_e = e = Gtk.Entry()
                e.connect("changed", self.search_main_cb)
                e.connect("icon-press", lambda x, y, z : x.set_text(''))
                e.set_icon_from_stock(1, Gtk.STOCK_FIND)
                e.set_can_default(True)
                h.pack_end(e, False, False, 6)
                h.show_all()
                self.GoMain_b.hide()

                # Main ScrolledWindow
                self.main_container = ms = Gtk.ScrolledWindow()
                ms.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
                self.pack_start(ms, True, True, 6)

                # Main contianer
                mvb = Gtk.VBox(False,2)
                ms.add_with_viewport(mvb)
                ms.show_all()

                # Sub ScrolledWindow
                self.sub_container = ss = Gtk.ScrolledWindow()
                ss.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
                self.pack_start(ss, True, True, 6)

                # Sub container
                svb = Gtk.VBox(False, 2)
                ss.add_with_viewport(svb)
                #ss.show()
                svb.show()

                for i in categories.ls:
                        self.__newCat(i)

                self.__loadPlugins(skip)
                self.show()

        def show_about_dlg(self, *w):
                return OCCAbout(self.ccw)
        
        def __newCat(self,i):
                mvb = self.main_container.get_children()[0].get_children()[0]
                if type(i)==str:
                        k = i
                        r = CatFrame(i)
                else:
                        k = i[0]
                        r = CatFrame(*i)
                mvb.pack_start(r, False, False, 2)
                mvb.show_all()
                self.cat_v[k]=r
                self.cat_plugins[k]=[]
                return r
        
        def __loadPlugins(self, skip):
                p = self.Loader.get_plugins()
                p.sort(lambda a,b: a['priority'] - b['priority'])
                btncnt = dict((i[0],[0, Gtk.Fixed(), False]) for i in categories.ls)
                
                svb = self.sub_container.get_children()[0].get_children()[0]

                for i in p:
                        category = i['category']
                        if category in btncnt:
                                btncnt[category][0] += 1
                        else:
                                btncnt[category][0] = 0
                
                        if btncnt[category][0] % 6 == 0:
                                btncnt[category][0] = 1
                                btncnt[category][1] = Gtk.Fixed()
                                btncnt[category][2] = False
                
                        h = btncnt[category][1]
                        if not btncnt[category][2]:
                                btncnt[category][2] = True
                                try: self.cat_v[category].pack_start(h,False,False,0)
                                except KeyError: self.__newCat(category).pack_start(h,False,False,0)
                        # pack main buttons
                        mb = self.create_buttons(i, svb)
                        h.put(mb, (btncnt[category][0]-1)*125, 0)
                        h.show_all()
                        # pack plugin
                        #print category, i, btncnt[category][0]
                        #svb.pack_start(i,False,False,0)
                        self.cat_plugins[category].append(i)
                        self.create_search_dict(mb, i)
                
        def create_search_dict(self, button, plugin):
                caption = plugin['caption'].replace(':', '').lower()
                description = plugin['description'].lower()

                self.cat_buttons[button] = {'caption': caption,
                                                                        'description': description,
                                                                        'category': plugin['category']}
                                                        
        def create_buttons(self, plugin, vb):
                # we must remove char : in the caption ?
                caption = plugin['caption'].replace(':', '')
                # FIXME: make fixed size main button widget
                b=MainButton(caption, icon='ojuba-control-center') #stock=Gtk.STOCK_PREFERENCES)
                b.set_tooltip_text(caption)
                #b.connect('clicked', self.show_plugin, caption)
                #b.connect('activate-link', self.show_plugin, caption)
                b.connect("button-press-event", self.show_plugin, plugin['name'], vb)
                return b

        def show_plugin(self, b, e, plugin, vb):
                
                if e.button > 1:
                        return
                for p in self.vis_plugins:
                        p.hide()
                
                self.searh_e.set_text('')
                self.searh_e.hide()
                if type(plugin) == dict:
                        plugin = plugin['name']
                p = self.Loader.load_plugin(plugin)
                # TODO: raise if object faild
                try:
                        if not p[0]:
                                vb.pack_start(p[1],False,False,6)
                except IndexError: 
                        print 'Import Error:', plugin
                        return 
                p = p[1]
                p.show_all()
                self.vis_plugins.append(p)
                self.GoMain_b.show_all()
                self.main_container.hide()
                self.sub_container.show()
                self.ccw.set_title(p.caption.replace(':', ''))
                return False
    
        def show_main_cb(self, *b):
                self.searh_e.show()
                self.searh_e.set_text('')

                self.GoMain_b.hide()
                self.sub_container.hide()
                self.main_container.show_all()
                for p in self.vis_plugins:
                        p.hide()
                self.vis_plugins = []
                self.ccw.set_title(_('Ojuba Control Center'))
                self.searh_e.grab_focus()
    
        def search_main_cb(self, e):
                txt = e.get_text().lower()
                if not txt:
                        e.set_icon_from_stock(1, Gtk.STOCK_FIND)
                        self.main_container.show_all()
                        return
                e.set_icon_from_stock(1, Gtk.STOCK_CLEAR)
                d = self.cat_buttons
                l = filter(lambda a: txt in d[a]['caption'] or txt in d[a]['description'], d.keys())
                cats = []
                for p in self.cat_buttons.keys():
                        #self.cat_v[k]=r
                        cat = d[p]['category']
                        if p in l:
                            p.show()
                            self.cat_v[cat].show()
                            cats.append(cat)
                        else:
                            p.hide()
                            if cat not in cats:
                                    self.cat_v[cat].hide()
                        
class OCCAbout(Gtk.AboutDialog):
        def __init__(self, parent):
                Gtk.AboutDialog.__init__(self, parent=parent)
                self.set_default_response(Gtk.ResponseType.CLOSE)
                #self.connect('delete-event', self.__hide_cb)
                #self.connect('response', self.__hide_cb)
                try: self.set_program_name("OCC")
                except: pass
                self.set_name(_("OCC"))
                #self.about_dlg.set_version(version)
                self.set_copyright("Copyright © 2009 ojuba.org")
                self.set_comments(_("Ojuba Control Center"))
                self.set_license("""\
                Released under terms of Waqf Public License.
                This program is free software; you can redistribute it and/or modify
                it under the terms of the latest version Waqf Public License as
                published by Ojuba.org.

                This program is distributed in the hope that it will be useful,
                but WITHOUT ANY WARRANTY; without even the implied warranty of
                MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

                The Latest version of the license can be found on
                "http://waqf.ojuba.org/"
                """)
                self.set_website("http://linux.ojuba.org")
                self.set_website_label("ojuba Linux web site")
                self.set_authors(["Muayyad Saleh Alsadi <alsadi@ojuba.org>", "Ehab El-Gedawy <ehabsas@gmail.com>"])
                self.run()
                self.destroy()
