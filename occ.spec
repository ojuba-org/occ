%global owner ojuba-org
%global commit #Write commit number here

Name:           occ
Version:        3.0.0
Release:        1%{?dist}
Summary:        Ojuba Control Center

Group:          Development/Languages
License:	WAQFv2
URL:            http://ojuba.org
Source:		https://github.com/%{owner}/%{name}/archive/%{commit}/%{name}-%{commit}.tar.gz

BuildArch:      noarch
Requires:       hda-verb
Requires:       ayat-repo
Requires:       usb_modeswitch
Requires:       xdg-utils
Requires:       system-switch-displaymanager
Requires:       glx-utils
Requires:       python-slip-dbus
Requires:       udisks
Requires:       PackageKit
Requires:       system-config-network
Requires:	pygobject3 >= 3.0.2
Obsoletes:	media-repo
BuildRequires:  python2-devel

%description
Ojuba Control Center is a central place to control your computer.

%prep
%setup -q -n %{name}-%{commit}

%build
make %{?_smp_mflags}

%install
%makeinstall DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/usr/sbin/

# local is used because we fix files from other packages, this is wrong but we do not have skype source to fix it
mkdir -p $RPM_BUILD_ROOT/usr/local/bin/ 

echo -e '#! /bin/sh\n[ $UID -ne 0 ] && echo -e "Permission denied, be root" && exit\nsetenforce 0\nsed -rie "s/^(SELINUX=).*/\1disabled/" /etc/selinux/config' >$RPM_BUILD_ROOT/usr/sbin/sestop

echo -e '#! /bin/sh\nLD_PRELOAD=/usr/lib/libv4l/v4l1compat.so exec RunOrInstall skype /usr/bin/skype "$@"' >$RPM_BUILD_ROOT/usr/local/bin/skype
echo -e '#! /bin/sh\nLC_ALL=en_US.UTF-8 exec RunOrInstall audacity-freeworld /usr/bin/audacity "$@"' >$RPM_BUILD_ROOT/usr/local/bin/audacity

chmod +x $RPM_BUILD_ROOT/usr/local/bin/*
chmod +x $RPM_BUILD_ROOT/usr/sbin/*

%post
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS README COPYING waqf2-ar.pdf
%{python2_sitelib}/*
/etc/dbus-1/system.d/org.Ojuba.OCC.conf
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/ojuba-control-center.svg
%{_datadir}/icons/hicolor/*/apps/ojuba-control-center.png
%{_datadir}/polkit-1/actions/org.ojuba.occ.policy
%{_datadir}/dbus-1/system-services/org.Ojuba.OCC.service
%{_datadir}/occ/occ-mechanism.py*
%{_datadir}/occ/mechanisms/*.py*
%{_datadir}/occ/Plugins/*.py*
%{_datadir}/occ/icons/*.*
%{_datadir}/locale/*/*/*.mo
%{_bindir}/*
%{_sbindir}/*
/usr/local/bin/*


%changelog
* Sun Mar 16 2014 Mosaab Alzoubi <moceap@hotmail.com> - 3.0.0-1
- Update to 3.0.

* Fri Feb 21 2014 Mosaab Alzoubi <moceap@hotmail.com> - 2.0.0-3
- alsa-tools provide hda-verb since 2012.

* Sun Feb 16 2014 Mosaab Alzoubi <moceap@hotmail.com> - 2.0.0-2
- General Revision.

* Sat Aug 10 2013  Ehab El-Gedawy <ehabsas@gmail.com> - 2.0.0-1
- dbus call fix
- load mechanisms 

* Sat Jun 2 2012  Muayyad Saleh AlSadi <alsadi@ojuba.org> - 1.22.4-1
- port to gtk3, webkit3

* Wed Jul 13 2011 Muayyad Saleh Alsadi <alsadi@ojuba.org> - 1.20.0-1
- some gnome-shell features

* Sun Jun 27 2010 Muayyad Saleh Alsadi <alsadi@ojuba.org> - 1.10.4-1
- don't show PAE kernels in x86_64

* Sun Jun 20 2010 Muayyad Saleh Alsadi <alsadi@ojuba.org> - 1.10.3-1
- requires hda-verb

* Thu May 27 2010 Muayyad Saleh Alsadi <alsadi@ojuba.org> - 1.10.2-1
- port to Fedora 13

* Thu Nov 26 2009 Muayyad Saleh Alsadi <alsadi@ojuba.org> - 1.9.10-1
- add wide LCD resolutions

* Tue Nov 24 2009 Muayyad Saleh Alsadi <alsadi@ojuba.org> - 1.9.9-1
- fix a bug in the case of unknown nvidia vga

* Sun Oct 4 2009 Muayyad Saleh Alsadi <alsadi@ojuba.org> - 1.9.8-1
- add --skip-plugins option
- add xorgconf plugin

* Wed Sep 30 2009 Muayyad Saleh Alsadi <alsadi@ojuba.org> - 1.9.6-1
- bug fixes in usbsw.py

* Thu Sep 3 2009 Muayyad Saleh Alsadi <alsadi@ojuba.org> - 1.9.1-1
- bug fixes
- disable/enable net repos

* Sat Aug 29 2009 Muayyad Saleh Alsadi <alsadi@ojuba.org> - 1.9.0-1
- manage samples icon
- add installer tab

* Sun Aug 16 2009 Muayyad Saleh Alsadi <alsadi@ojuba.org> - 1.8.1-1
- add plugin for slmodem

* Sun Aug 16 2009 Muayyad Saleh Alsadi <alsadi@ojuba.org> - 1.7.0-1
- add more features: network, samba, legacy2opentype, autologin, pulse, boot

* Fri Aug 7 2009 Muayyad Saleh Alsadi <alsadi@ojuba.org> - 1.6.0-1
- all plugins and mechanisms are fully functional

* Fri Jun 26 2009 Muayyad Saleh Alsadi <alsadi@ojuba.org> - 1.1.0-1
- initial package
