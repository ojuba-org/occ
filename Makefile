APPNAME=occ
L_APPNAME=OjubaControlCenter
ICON_NAME=ojuba-control-center
DESTDIR?=/
DATADIR?=$(DESTDIR)/usr/share

SOURCES=$(wildcard *.desktop.in)
TARGETS=${SOURCES:.in=}

ECHO := echo
MAKE := make
PYTHON := python2
INSTALL := install
INTLTOOL_MERGE := intltool-merge
RM := $(shell which rm | egrep '/' | sed  's/\s//g')
GTK_UPDATE_ICON_CACHE := $(shell which gtk-update-icon-cache)
UPDATE_DESKTOP_DATABASE := $(shell which update-desktop-database)

all: $(TARGETS) micons

micons:
	@$(ECHO) "*** Converting: icons..."
	@for i in 96 72 64 48 36 32 24 22 16; do \
		convert -background none $(ICON_NAME).svg -resize $${i}x$${i} $(ICON_NAME)-$${i}.png; \
	done

pos:
	$(MAKE) -C po all

install-dbus-conf:
	@$(ECHO) "*** Installing: D-Bus config files..."
	@$(INSTALL) -d $(DESTDIR)/etc/dbus-1/system.d/
	@$(INSTALL) -m 0644 config/org.Ojuba.OCC.conf $(DESTDIR)/etc/dbus-1/system.d/
	@$(INSTALL) -d $(DESTDIR)/usr/share/dbus-1/system-services/
	@$(INSTALL) -m 0644 config/org.Ojuba.OCC.service $(DESTDIR)/usr/share/dbus-1/system-services/
	@$(INSTALL) -d $(DESTDIR)/usr/share/polkit-1/actions/
	@$(INSTALL) -m 0644 config/org.ojuba.occ.policy $(DESTDIR)/usr/share/polkit-1/actions/

install: install-dbus-conf locale
	@$(ECHO) "*** Installing..."
	@#$(PYTHON)  -m compileall -fi {Plugins,mechanisms}/*.py
	@#$(PYTHON)  -Om compileall -fi {Plugins,mechanisms}/*.py
	@$(PYTHON) setup.py install -O2 --root $(DESTDIR)
	@$(ECHO) "Copying: $(APPNAME).desktop -> $(DATADIR)/applications/"
	@$(INSTALL) -d $(DATADIR)/applications/
	@$(INSTALL) -d $(DATADIR)/$(APPNAME)/
	@$(INSTALL) -m 0644 $(APPNAME).desktop $(DATADIR)/applications/
	@$(INSTALL) -m 0644 -D $(ICON_NAME).svg $(DATADIR)/icons/hicolor/scalable/apps/$(ICON_NAME).svg;
	@for i in 96 72 64 48 36 32 24 22 16; do \
		$(INSTALL) -d $(DATADIR)/icons/hicolor/$${i}x$${i}/apps; \
		$(INSTALL) -m 0644 -D $(ICON_NAME)-$${i}.png $(DATADIR)/icons/hicolor/$${i}x$${i}/apps/$(ICON_NAME).png; \
	done
	@$(RM) -rf build
	@$(DESTDIR)/$(UPDATE_DESKTOP_DATABASE) --quiet $(DATADIR)/applications  &> /dev/null || :
	@$(DESTDIR)/$(GTK_UPDATE_ICON_CACHE) --quiet $(DATADIR)/icons/hicolor &> /dev/null || :

uninstall-dbus-conf:
	@$(ECHO) "*** Uninstalling: D-Bus config files..."
	@$(ECHO) "- Removing: $(DESTDIR)/etc/dbus-1/system.d/org.Ojuba.OCC.conf"
	@$(RM) -f $(DESTDIR)/etc/dbus-1/system.d/org.Ojuba.OCC.conf
	@$(ECHO) "- Removing: $(DESTDIR)/usr/share/dbus-1/system-services/org.Ojuba.OCC.service"
	@$(RM) -f $(DESTDIR)/usr/share/dbus-1/system-services/org.Ojuba.OCC.service
	@$(ECHO) "- Removing: $(DESTDIR)/usr/share/polkit-1/actions/org.ojuba.occ.policy"
	@$(RM) -f $(DESTDIR)/usr/share/polkit-1/actions/org.ojuba.occ.policy

uninstall: uninstall-dbus-conf
	@$(ECHO) "*** Uninstalling..."
	@$(ECHO) "- Removing: $(DATADIR)/applications/$(APPNAME).desktop"
	@$(RM) -f $(DATADIR)/applications/$(APPNAME).desktop
	@$(ECHO) "- Removing: $(DESTDIR)/usr/share/locale/*/LC_MESSAGES/$(APPNAME).mo"
	@$(RM) -f $(DESTDIR)/usr/share/locale/*/LC_MESSAGES/$(APPNAME).mo
	@$(ECHO) "- Removing: $(DESTDIR)/usr/bin/$(APPNAME)"
	@$(RM) -f $(DESTDIR)/usr/bin/$(APPNAME)-gtk
	@$(ECHO) "- Removing: $(DESTDIR)/usr/lib/python*/*-packages/$(L_APPNAME)"
	@$(RM) -rf $(DESTDIR)/usr/lib/python*/*-packages/$(L_APPNAME)
	@$(ECHO) "- Removing: $(DESTDIR)/usr/lib/python*/*-packages/$(APPNAME)*"
	@$(RM) -rf $(DESTDIR)/usr/lib/python*/*-packages/$(APPNAME)*
	@$(ECHO) "- Removing: $(DESTDIR)/usr/share/$(APPNAME)"
	@$(RM) -rf $(DESTDIR)/usr/share/$(APPNAME)
	
	@$(ECHO) "- Removing: $(DESTDIR)/usr/*/share/locale/*/LC_MESSAGES/$(APPNAME).mo"
	@$(RM) -f $(DESTDIR)/usr/*/share/locale/*/LC_MESSAGES/$(APPNAME).mo
	@$(ECHO) "- Removing: $(DESTDIR)/usr/*/bin/$(APPNAME)"
	@$(RM) -f $(DESTDIR)/usr/*/bin/$(APPNAME)-gtk
	@$(ECHO) "- Removing: $(DESTDIR)/usr/*/lib/python*/*-packages/$(L_APPNAME)"
	@$(RM) -rf $(DESTDIR)/usr/*/lib/python*/*-packages/$(L_APPNAME)
	@$(ECHO) "- Removing: $(DESTDIR)/usr/*/lib/python*/*-packages/$(APPNAME)*"
	@$(RM) -rf $(DESTDIR)/usr/*/lib/python*/*-packages/$(APPNAME)*
	@$(ECHO) "- Removing: $(DESTDIR)/usr/*/share/$(APPNAME)"
	@$(RM) -rf $(DESTDIR)/usr/*/share/$(APPNAME)
	@$(RM) -r $(DESTDIR)/usr/bin/{$(APPNAME),RunOrInstall,legacy2opentype}
	@$(RM) -f $(DATADIR)/icons/hicolor/scalable/apps/$(ICON_NAME).svg
	@$(RM) -f $(DATADIR)/icons/hicolor/*/apps/$(ICON_NAME).png;
	@$(DESTDIR)/$(UPDATE_DESKTOP_DATABASE) --quiet $(DATADIR)/applications  &> /dev/null || :
	@$(DESTDIR)/$(GTK_UPDATE_ICON_CACHE) --quiet $(DATADIR)/icons/hicolor &> /dev/null || :
	
%.desktop: %.desktop.in pos
	intltool-merge -d po $< $@

clean:
	@$(ECHO) "*** Cleaning..."
	@$(MAKE) -C po clean
	@$(ECHO) "- Removing: $(TARGETS)"
	@$(RM) -f $(TARGETS)
	@$(ECHO) "- Removing: locale build"
	@$(RM) -rf locale build
	@$(ECHO) "- Removing: *.py[co]"
	@find . -iname '*.pyc' -exec rm -f {} \;
	@find . -iname '*.pyo' -exec rm -f {} \;
	@$(ECHO) "- Removing: $(ICON_NAME)-*.png"
	@$(RM) -f $(ICON_NAME)-*.png
	
