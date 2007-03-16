Name:           linphone
Version:        1.6.0
Release:        4%{?dist}
Summary:        Phone anywhere in the whole world by using the Internet

Group:          Applications/Communications
License:        GPL
URL:            http://www.linphone.org/
Source0:        http://download.savannah.nongnu.org/releases/linphone/1.6.x/sources/%{name}-%{version}.tar.gz
Patch:          linphone-1.0.1-desktop.patch
Patch1:         linphone-1.4.1-libs.patch
Patch2:         linphone-1.5.1-osipcompat.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  compat-libosip2-devel
BuildRequires:  ortp-devel = 0.13.0

BuildRequires:  readline-devel
BuildRequires:  ncurses-devel

BuildRequires:  gnome-panel-devel
BuildRequires:  libgnomeui-devel
BuildRequires:  glib2-devel
BuildRequires:  alsa-lib-devel

BuildRequires:  speex-devel >= 1.2

BuildRequires:  desktop-file-utils

BuildRequires:  perl(XML::Parser)

BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  intltool
BuildRequires:  gettext

%description
Linphone is mostly sip compliant. It works successfully with these
implementations:
    * eStara softphone (commercial software for windows)
    * Pingtel phones (with DNS enabled and VLAN QOS support disabled).
    * Hotsip, a free of charge phone for Windows.
    * Vocal, an open source SIP stack from Vovida that includes a SIP proxy
        that works with linphone since version 0.7.1.
    * Siproxd is a free sip proxy being developed by Thomas Ries because he
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

%prep
%setup0 -q
%patch0 -p1 -b .old
%patch1 -p1 -b .libs
%patch2 -p0 -b .osip

rm -r oRTP

pushd share/cs
for f in *.1
do
        /usr/bin/iconv --from-code iso-8859-2 --to-code utf-8 --output $f.new $f && sed -i -e 's/Encoding: ISO-8859-2/Encoding: UTF-8/' $f.new && mv $f.new $f
done
popd

%build
libtoolize --copy --force
aclocal -I m4
autoheader
automake --force-missing --add-missing --copy
autoconf
rm -rf config.cache

pushd mediastreamer2
libtoolize --copy --force
aclocal
autoheader
automake --force-missing --add-missing --copy
autoconf
popd

%configure --disable-static --disable-video
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
install -p -m 0644 pixmaps/linphone2.png $RPM_BUILD_ROOT%{_datadir}/pixmaps
%find_lang %{name}
rm $RPM_BUILD_ROOT%{_datadir}/gnome/apps/Internet/linphone.desktop
desktop-file-install --vendor=fedora \
  --delete-original \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --remove-category Application \
  --add-category Telephony \
  --add-category GTK \
  $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop
rm -f %{buildroot}%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%{_bindir}/*
%{_libdir}/bonobo/servers/*.server
%{_libdir}/liblinphone.so.*
%{_libdir}/libmediastreamer.so.*
%{_libdir}/libquickstream.so.*
%{_libexecdir}/*
%{_mandir}/man1/*
%lang(cs) %{_mandir}/cs/man1/*
%{_datadir}/applications/*%{name}.desktop
%{_datadir}/gnome/help/linphone
%{_datadir}/gnome-2.0/ui/*.xml
%{_datadir}/pixmaps/linphone
%{_datadir}/pixmaps/linphone2.png
%{_datadir}/sounds/linphone

%files devel
%defattr(-,root,root)
%{_includedir}/linphone
%{_includedir}/mediastreamer2
%{_libdir}/liblinphone.so
%{_libdir}/libmediastreamer.so
%{_libdir}/libquickstream.so
%{_libdir}/pkgconfig/*

%changelog
* Fri Mar 16 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.6.0-4
- Fix up encodings in Czech manpages

* Fri Mar 16 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.6.0-3
- Move autoheader after aclocal, fixes 232592

* Mon Jan 29 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.6.0-2
- Fix buildrequires

* Mon Jan 29 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.6.0-1
- Update to 1.6.0

* Wed Nov 22 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.5.1-2
- Mark translated man pages with lang macro

* Tue Nov 21 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.5.1-1
- Update to 1.5.1

* Thu Oct 26 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.5.0-2
- Don't forget to add new files and remove old ones!

* Thu Oct 26 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.5.0-1
- Update to 1.5.0
- Fix spelling error in description.
- Remove invalid categories on desktop file.

* Wed Aug 30 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.2.0-7
- Bump release so that I can "make tag"

* Wed Aug 30 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.2.0-6
- Add BR for perl(XML::Parser) so that intltool will work.

* Wed Aug 30 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.2.0-5
- Bump release and rebuild.

* Mon Feb 13 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.0-2
- Rebuild for Fedora Extras 5

* Wed Feb  8 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.0-1
- Added version for speex-devel BR (#179879)

* Tue Jan 24 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.0-2
- Fixed selecting entry from address book (#177189)

* Tue Jan  3 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.0-1
- Upstream update

* Mon Dec  5 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.1.0-2
- Added version on ortp-devel

* Mon Dec  5 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.1.0-1
- Upstream update

* Wed Nov 30 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.0.1-5
- Remove ortp documentation for -devel

* Wed Nov 30 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.0.1-4
- Split out ortp

* Fri May 27 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.0.1-3
- Fix multiple menu entry and missing icon (#158975)
- Clean up spec file

* Fri May  6 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.0.1-2
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
