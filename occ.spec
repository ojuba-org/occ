# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           occ
Version:        1.20.1
Release:        1%{?dist}
Summary:        Ojuba Control Center

Group:          Development/Languages
License:        waqf
URL:            http://linux.ojuba.org
Source0:        %{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
Requires:       hda-verb usb_modeswitch xdg-utils system-switch-displaymanager glx-utils python-slip-dbus udisks PackageKit system-config-network
Obsoletes:	media-repo
BuildRequires:  python-devel
%description
Ojuba Control Center is a central place to control your computer.

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/usr/local/bin/

echo -e '#! /bin/sh\nLC_ALL=en_US.UTF-8 exec RunOrInstall audacity-freeworld /usr/bin/audacity "$@"' >$RPM_BUILD_ROOT/usr/local/bin/audacity
echo -e '#! /bin/sh\nlib=`[[ $( arch ) -eq x86_64 ]] && echo "lib64" || echo "lib"`\nLD_PRELOAD=/usr/$lib/libv4l/v4l1compat.so exec RunOrInstall skype /usr/bin/skype "$@"' >$RPM_BUILD_ROOT/usr/local/bin/skype
chmod +x $RPM_BUILD_ROOT/usr/local/bin/*

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS README COPYING LICENSE-ar.txt LICENSE-en
%{python_sitelib}/*
/etc/dbus-1/system.d/org.ojuba.occ.conf
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/ojuba-control-center.svg
%{_datadir}/polkit-1/actions/org.ojuba.occ.policy
%{_datadir}/dbus-1/system-services/org.ojuba.occ.service
%{_datadir}/occ/occ-mechanism.py*
%{_datadir}/occ/mechanisms/*.py*
%{_datadir}/occ/Plugins/*.py*
%{_datadir}/locale/*/*/*.mo
%{_bindir}/*
/usr/local/bin/*


%changelog
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

* Sun Aug 29 2009 Muayyad Saleh Alsadi <alsadi@ojuba.org> - 1.9.0-1
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

