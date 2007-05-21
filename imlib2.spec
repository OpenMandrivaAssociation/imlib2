%define	name	imlib2
%define	version	1.4.0
%define release	%mkrel 1
%define major	1
%define libname	%mklibname %{name}_ %{major}
%define enable_mmx 0
%{?_with_mmx: %global enable_mmx 1}

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Powerful image loading and rendering library
License:	BSD
URL:		http://enlightenment.org/Libraries/Imlib2/
Group:		System/Libraries
BuildRoot:	%{_tmppath}/%{name}-%{version}

Source0:	http://prdownloads.sourceforge.net/enlightenment/%{name}-%{version}.tar.bz2
Patch0:		imlib2-1.2.2-64bit-tiff-loader.patch
BuildRequires:	freetype2-devel
BuildRequires:	jpeg-devel
BuildRequires:	png-devel
BuildRequires:	libtiff-devel
BuildRequires:	ungif-devel
BuildRequires:	X11-devel

%description
Imlib2 is an advanced replacement library for libraries like libXpm that
provides many more features with much greater flexibility and speed than
standard libraries, including font rasterization, rotation, RGBA space
rendering and blending, dynamic binary filters, scripting, and more.

Build Options:
--with mmx      Enable mmx cpu detection (10% - 30% speedup)

%package -n	%{libname}
Summary:	Powerful image loading and rendering library
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Requires:	%{libname}-filters = %{version}-%{release}
Requires:	%{libname}-loaders = %{version}-%{release}

%description -n	%{libname}
Imlib2 is an advanced replacement library for libraries like libXpm that
provides many more features with much greater flexibility and speed than
standard libraries, including font rasterization, rotation, RGBA space
rendering and blending, dynamic binary filters, scripting, and more.


%package -n	%{libname}-devel
Summary:	Imlib2 headers, static libraries and documentation
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

%description -n	%{libname}-devel
Imlib2 is an advanced replacement library for libraries like libXpm that
provides many more features with much greater flexibility and speed than
standard libraries, including font rasterization, rotation, RGBA space
rendering and blending, dynamic binary filters, scripting, and more.

This package contains various headers and static libraries for %{name}.
You need this package if you want to compile or develop any applications
that need %{name}.


%package -n	%{libname}-filters
Summary:	Imlib2 basic plugin filters set
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description -n	%{libname}-filters
This package contains Imlib2 basic set of plugin filters.


%package -n	%{libname}-loaders
Summary:	Imlib2 loader for various graphic formats
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description -n	%{libname}-loaders
This package contains Imlib2 image loader/saver for various graphic formats,
such as jpeg, gif, tiff, xpm etc.

%package data
Summary:	Imlib2 data
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description data
This package contains Imlib2 data.

%prep
%setup -q
#%patch0 -p1 -b .64bit

%build
%configure2_5x \
%if %enable_mmx
	--enable-mmx=yes \
%else
	--enable-mmx=no \
%endif

%make

%install
rm -rf %{buildroot}
%makeinstall_std

# remove files not bundled
rm -f	%{buildroot}%{_libdir}/%{name}/loaders/*.a \
	%{buildroot}%{_libdir}/%{name}/filters/*.a

%multiarch_binaries %{buildroot}%{_bindir}/imlib2-config

%clean
rm -rf %{buildroot}

%post  -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root,0755)
%doc AUTHORS README COPYING
%{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(-,root,root,0755)
%doc AUTHORS README COPYING ChangeLog doc/index.html doc/imlib2.gif doc/blank.gif
%{_bindir}/*
%multiarch %{_bindir}/imlib2-config
%{_libdir}/lib*.so
%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*

%files -n %{libname}-filters
%defattr(-,root,root)
%doc AUTHORS README COPYING
%{_libdir}/%{name}/filters

%files -n %{libname}-loaders
%defattr(-,root,root)
%doc AUTHORS README COPYING
%{_libdir}/%{name}/loaders

%files data
%defattr(-,root,root)
%doc AUTHORS README COPYING
%{_datadir}/%{name}

%changelog
* Wed May 16 2007 Antoine Ginies <aginies@mandriva.com> 1.4.0-1mdv2008.0
- 1.4.0 release

* Fri Jul 21 2006 Stew Benedict <sbenedict@mandriva.com> 1.2.2-3mdv2006.0
- P0: fix for 64bit crash in tiff loader (#22355)

* Wed May 10 2006 Thierry Vignaud <tvignaud@mandriva.com> 1.2.2-2mdk
- use %%mkrel
- fix URL

* Fri Mar 24 2006 Austin Acton <austin@mandriva.org> 1.2.2-1mdk
- New release 1.2.2

* Sat Dec 31 2005 Mandriva Linux Team <http://www.mandrivaexpert.com/> 1.2.1-2mdk
- Rebuild

* Tue Jun 28 2005 Guillaume Rousse <guillomovitch@mandriva.org> 1.2.1-1mdk 
- new release
- spec cleanup
- dropped patches, problems fixed upstream

* Thu Mar 24 2005 Guillaume Rousse <guillomovitch@mandrake.org> 1.2.0-3mdk 
- fix issue with dynamic loading that broke perl bindings (patch stolen from Debian, see http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=293815)

* Thu Feb 10 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.2.0-2mdk
- lib64 fixes

* Wed Jan 26 2005 Guillaume Rousse <guillomovitch@mandrake.org> 1.2.0-1mdk 
- new release
- rpmbuildupdate aware
- drop all patches (merged upstream)
- data subpackage
- multiarch fix

* Fri Oct 08 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 1.1.0-4mdk
- Patch2: security fix for BMP crasher

* Tue Jun 08 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.1.0-3mdk
- fix gcc-3.4 patch (P1)

* Tue Jun 08 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.1.0-2mdk
- fix gcc-3.4 build (P1)

* Thu May 27 2004 Abel Cheung <deaddog@deaddog.org> 1.1.0-1mdk
- New version
- Redo patch0 (sing along: "libtool, bang bang...")

* Tue Sep  2 2003 Abel Cheung <deaddog@deaddog.org> 1.0.6-4mdk
- mklibname
- remove RPM_BUILD_ROOT in install instead of prep
- remove various static module files not under $libdir
- remove packager tag
- how can rasterman's stuff be GPL'ed
- strip redundant BuildRequires and Requires
- configure2_5x, makeinstall_std
- DIRM fix
- remove duplicates in file lists
- convert this spec to UTF-8
- rpmlint fix (avoid non-pic library by overwriting libtool stuff with
  libtoolize)
- Patch0: Avoid /home in .la files
- Where should /usr/lib/loaders go? Can't please both distriblint and
  rpmlint

* Sat Jul 12 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.0.6-3mdk
- rebuild

* Fri Dec 06 2002 Vincent Guardiola <vguardiola@mandrakesoft.com> 1.0.6-2mdk
- Add Requires
- Clean spec file

* Fri Dec 06 2002 Vincent Guardiola <vguardiola@mandrakesoft.com> 1.0.6-1mdk
- - Release 1.0.6
- Fixing bad path in la files

* Fri Jun 14 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.0.5-2mdk
- rebuild for libintl2
- BuildConflicts freetds-devel

* Mon Mar 25 2002 Vincent Guardiola <vguardiola@mandrakesoft.com> 1.0.5-1mdk
- - Release 1.0.5

* Wed Jan 23 2002 Yves Duret <yduret@mandrakesoft.com> 1.0.4-3mdk
- --disable-mmx in %%configure
- mandrakezicacion: macros and macros and macros

* Mon Jan 21 2002 Stefan van der Eijk <stefan@eijk.nu> 1.0.4-2mdk
- BuildRequires

* Wed Nov 28 2001 Vincent Guardiola  <vguardiola@mandrakesoft.com> 1.0.4-1mdk
- Initial package for MDK

* Tue Aug 28 2001 Alvaro Herrera <alvherre@dcc.uchile.cl>
- Remove loader_db since it's included in a different package.

* Mon Jan 8 2001 The Rasterman <raster@rasterman.com>
- Fix Requires & BuildRequires for freetype.

* Sat Sep 30 2000 Lyle Kempler <term@kempler.net>
- Bring back building imlib2 as root via autogen.sh for the lazy (me)
- Some minor changes

* Sat Sep 30 2000 Joakim Bodin <bodin@dreamhosted.com>
- Linux-Mandrake:ise the spec file

* Tue Sep 12 2000 The Rasterman <raster@rasterman.com>
- Redo spec file

* Wed Aug 30 2000 Lyle Kempler <kempler@utdallas.edu>
- Include imlib2-config

* Sat May 20 2000 Lyle Kempler <kempler@utdallas.edu>
- Fixed problems with requiring imlib2_view
- Went back to imlib2_view (not imlib2-view)

* Tue Nov 2 1999 Lyle Kempler <kempler@utdallas.edu>
- Mangled imlib 1.9.8 imlib spec file into imlib2 spec file
