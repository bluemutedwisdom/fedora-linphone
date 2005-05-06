%{!?dist: %define dist .fc4 }
%{!?fedora: %define fedora 4 }
Name:           linphone
Version:        1.0.1
Release:        2%{?dist}
Summary:        Phone anywhere in the whole world by using the Internet

Group:          Applications/Communications
License:        GPL
URL:            http://www.linphone.org/?lang=us&rubrique=1
Source0:        http://simon.morlat.free.fr/download/1.0.x/source/linphone-1.0.1.tar.gz
Patch:         linphone-1.0.1-pkgconfig.patch
Patch1:         linphone-1.0.1-Werror.patch
Patch2:         linphone-1.0.1-desktop.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gnome-panel-devel libgnomeui-devel glib2-devel alsa-lib-devel
BuildRequires:  libosip2-devel speex-devel gettext desktop-file-utils

%description
Linphone is mostly sip compliant. It works successfully with these
implementations:
    * eStara softphone (commercial software for windows)
    * Pingtel phones (with DNS enabled and VLAN QOS support disabled).
    * Hotsip, a free of charge phone for Windows.
    * Vocal, an open source SIP stack from Vovida that includes a SIP proxy
        that works with linphone since version 0.7.1.
    * Siproxd is a free sip proxy being developped by Thomas Ries because he
        would like to have linphone working behind his firewall. Siproxd is
        simple to setup and works perfectly with linphone.
    * Partysip aims at being a generic and fully functionnal SIP proxy. Visit
        the web page for more details on its functionalities.

Linphone may work also with other sip phones, but this has not been tested yet.

%package devel
Summary:        Development libraries for linphone
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release} glib2-devel

%description    devel
Libraries and headers required to develop software with linphone.

%package -n ortp
Summary:        A C library implementing the RTP protocol (rfc1889)
Group:          System Environment/Libraries
Version:        0.7.0

%description -n ortp
oRTP is a LGPL licensed C library implementing the RTP protocol (rfc1889). It
is available for most *nix clones (primilarly Linux and HP-UX), and Win32.

%package -n ortp-devel
Summary:        Development libraries for ortp
Group:          Development/Libraries
Version:        0.7.0

%description -n ortp-devel
Libraries and headers required to develop software with ortp.

%prep
%setup -q
%patch -p 1 -b .pkgconfig
%patch1 -p 1 -b .Werror
%patch2 -p 1 -b .old

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
%find_lang %{name}
desktop-file-install --vendor=fedora \
  --delete-original \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --remove-category Network \
  --add-category X-Fedora \
  --add-category Internet \
  --add-category Telephony \
  --add-category GTK \
  $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n ortp -p /sbin/ldconfig

%postun -n ortp -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%{_bindir}/*
%{_libdir}/bonobo/servers/*.server
%{_libdir}/liblinphone.so.*
%{_libexecdir}/*
%{_mandir}/man1/*
%{_datadir}/applications/*%{name}.desktop
%{_datadir}/gnome/apps/Internet/*.desktop
%{_datadir}/gnome/help/linphone
%{_datadir}/gnome-2.0/ui/*.xml
%{_datadir}/gtk-doc/html/mediastreamer
%{_datadir}/pixmaps/linphone
%{_datadir}/sounds/linphone

%files devel
%defattr(-,root,root)
%{_datadir}/gtk-doc/html/ortp
%{_includedir}/linphone
%{_libdir}/liblinphone.a
%{_libdir}/liblinphone.la
%{_libdir}/liblinphone.so
%{_libdir}/pkgconfig/*

%files -n ortp
%defattr(-,root,root)
%doc oRTP/AUTHORS oRTP/ChangeLog oRTP/COPYING oRTP/NEWS oRTP/README oRTP/TODO oRTP/
%{_libdir}/libortp.so.*

%files -n ortp-devel
%defattr(-,root,root)
%{_includedir}/ortp
%{_libdir}/libortp.a
%{_libdir}/libortp.la
%{_libdir}/libortp.so

%changelog
* Fri May  6 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.0.1-2.fc4
- Add disttag to Release

* Fri Apr  8 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.0.1-2
- Remove -Werror from configure for now
- Fix .desktop file to have Terminal=false instead of 0

* Thu Mar 24 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.0.1-1
- Upstream update
- Separated ortp
- Added %%doc

* Wed Mar 23 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.12.2-7
- pkgconfig and -devel fixes

* Wed Mar 23 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.12.2-6
- Fix build on x86_64

* Sat Mar 19 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.12.2-5
- %%

* Sat Mar 19 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.12.2-4
- Used %%find_lang
- Tightened up %%files
- Streamlined spec file

* Thu Mar 17 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.12.2-3
- Broke %%description at 80 columns

* Wed Mar 16 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.12.2-2
- Removed explicit Requires

* Tue Mar 15 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.12.2-1
- Bump release to 1
- Cleaned up the -docs and -speex patches

* Fri Jan 21 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0:0.12.2-0.iva.1
- Fixed a silly spec error

* Fri Jan 21 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0:0.12.2-0.iva.0
- Initial RPM release.
