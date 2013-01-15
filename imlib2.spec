%define major	1
%define libname	%mklibname %{name}_ %{major}
%define develname %mklibname %{name} -d

Name:		imlib2
Version:	1.4.5
Release:	4
Summary:	Powerful image loading and rendering library
License:	Imlib2
URL:		http://enlightenment.org/Libraries/Imlib2/
Group:		System/Libraries
# Same as upstream tarball except the copyright-breaking /data/fonts
# subdirectory is entirely removed - AdamW 2008/03
Source0:	http://sourceforge.net/projects/enlightenment/files/imlib2-src/%{version}/%{name}-%{version}.tar.bz2
Patch0:		imlib2-automake-1.13.patch
# Drop data/fonts from the build, it only contains copyright-
# infringing fonts - AdamW 2008/03 (#38258)
Patch4:		imlib2-1.4.2-fontclean.patch
BuildRequires:	jpeg-devel
BuildRequires:	tiff-devel
BuildRequires:	ungif-devel
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(id3tag)
BuildRequires:	bzip2-devel

%description
Imlib2 is an advanced replacement library for libraries like libXpm that
provides many more features with much greater flexibility and speed than
standard libraries, including font rasterization, rotation, RGBA space
rendering and blending, dynamic binary filters, scripting, and more.

%package -n %{libname}
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

%package -n %{develname}
Summary:	Imlib2 headers, development libraries and documentation
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
# (tv) only ever released major was 1, so keep smooth upgrading for old distro in future releases:
Obsoletes:	%mklibname %{name}_ 1 -d
# taken from fedora where the demos and data are simply removed
Obsoletes:	%{name}-data

%description -n	%{develname}
Imlib2 is an advanced replacement library for libraries like libXpm that
provides many more features with much greater flexibility and speed than
standard libraries, including font rasterization, rotation, RGBA space
rendering and blending, dynamic binary filters, scripting, and more.

This package contains various headers and development libraries for %{name}.
You need this package if you want to compile or develop any applications
that need %{name}.

%package -n %{libname}-filters
Summary:	Imlib2 basic plugin filters set
Group:		System/Libraries

%description -n	%{libname}-filters
This package contains Imlib2 basic set of plugin filters.

%package -n %{libname}-loaders
Summary:	Imlib2 loader for various graphic formats
Group:		System/Libraries

%description -n	%{libname}-loaders
This package contains Imlib2 image loader/saver for various graphic formats,
such as jpeg, gif, tiff, xpm etc.

%prep
%setup -q
%patch0 -p1 -b .am13~
%patch4 -p1 -b .font~
autoreconf -fi

%build
%configure2_5x \
	--disable-static \
%ifarch x86_64
	--enable-amd64 \
	--disable-mmx \
%endif
%ifarch ix86
	--disable-amd64 \
	--enable-mmx \
%endif
	--enable-visibility-hiding
%make

%install
%makeinstall_std

# remove demos and their dependencies
rm -f %{buildroot}%{_bindir}/imlib2_*
rm -rf %{buildroot}%{_datadir}/imlib2/data/

%multiarch_binaries %{buildroot}%{_bindir}/imlib2-config

%files -n %{libname}
%doc AUTHORS README COPYING
%{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%doc ChangeLog doc/index.html doc/imlib2.gif doc/blank.gif
%{multiarch_bindir}/imlib2-config
%{_bindir}/imlib2-config
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*

%files -n %{libname}-filters
%{_libdir}/%{name}/filters

%files -n %{libname}-loaders
%{_libdir}/%{name}/loaders


%changelog
* Tue Dec 27 2011 Matthew Dawkins <mattydaw@mandriva.org> 1.4.5-3
+ Revision: 745481
- needed to add back multiarch bindir
- rebuild
- cleaned up spec
- obsolete data pkg
- remove all .la files

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuilt against libtiff.so.5

* Mon Oct 10 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 1.4.5-1
+ Revision: 704031
- update to new version 1.4.5
- drop patch 5, fixed by upstream

* Fri Sep 23 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 1.4.4-4
+ Revision: 701099
- add buildrequires on bzip2-devel
- on x86_64 use amd64 specific optimizations in other case use only mmx
- protect major in file list
- do not build static libs
- Patch5: fix against libpng15

* Sat May 07 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.4.4-3
+ Revision: 671931
- make data package noarch
- don't duplicate docs in every sub-package
- clean out old junk
- don't disable mmx support, cpuid is used to detect mmx support for being able
  to use it or not, thus enabling it won't break on i586 without mmx :)
- fix some dependency loops

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1.4.4-2
+ Revision: 661672
- multiarch fixes

* Tue Aug 03 2010 Funda Wang <fwang@mandriva.org> 1.4.4-1mdv2011.0
+ Revision: 565300
- new version 1.4.4

* Sun Jan 10 2010 Oden Eriksson <oeriksson@mandriva.com> 1.4.2-3mdv2010.1
+ Revision: 488768
- rebuilt against libjpeg v8

* Sat Aug 15 2009 Oden Eriksson <oeriksson@mandriva.com> 1.4.2-2mdv2010.0
+ Revision: 416618
- rebuilt against libjpeg v7

* Fri Feb 06 2009 Funda Wang <fwang@mandriva.org> 1.4.2-1mdv2009.1
+ Revision: 338008
- update license
- New version 1.4.2

* Sat Dec 20 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.1.000-4mdv2009.1
+ Revision: 316779
- rebuild

* Wed Aug 20 2008 Funda Wang <fwang@mandriva.org> 1.4.1.000-3mdv2009.0
+ Revision: 274336
- add patch fixing CVE-2008-2426

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 1.4.1.000-2mdv2009.0
+ Revision: 264684
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sun Jun 01 2008 Funda Wang <fwang@mandriva.org> 1.4.1.000-1mdv2009.0
+ Revision: 213939
- New version 1.4.1.000

* Thu Mar 06 2008 Adam Williamson <awilliamson@mandriva.org> 1.4.0.003-4mdv2008.1
+ Revision: 180284
- really use regenerated tarball, add necessary extra bit to fontclean.patch
- drop non-freely-licensed font files (#38258):
  	+ fontclean.patch: patches build process not to look for fonts dir
  	+ regenerate tarball without the offending directory

* Sun Jan 13 2008 Thierry Vignaud <tv@mandriva.org> 1.4.0.003-3mdv2008.1
+ Revision: 150286
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Vincent Guardiola <vguardiola@mandriva.com>
    - Test upload

* Fri Sep 14 2007 Michael Scherer <misc@mandriva.org> 1.4.0.003-2mdv2008.0
+ Revision: 85473
- add security fixes from #27005

  + Antoine Ginies <aginies@mandriva.com>
    - fix source
    - CVS SNAPSHOT 20070830, release 1.4.0.003

* Mon Jun 25 2007 Thierry Vignaud <tv@mandriva.org> 1.4.0.000-4mdv2008.0
+ Revision: 44019
- new devel library policy

* Tue May 29 2007 Antoine Ginies <aginies@mandriva.com> 1.4.0.000-3mdv2008.0
+ Revision: 32618
- CVS SNAPSHOT 20070529, release 1.4.0.000

* Thu May 24 2007 Antoine Ginies <aginies@mandriva.com> 1.4.0.000-2mdv2008.0
+ Revision: 30650
- increase release to get the good SRPM uploaded
- adjust version
- fix an error in spec file (Version: was updated instead of the macro version)

* Thu May 24 2007 Antoine Ginies <aginies@mandriva.com> 1.4.0.000-1mdv2008.0
+ Revision: 30616
- CVS snapshot 20070524, release 1.4.0.000
- remove unwanted changelog

* Mon May 21 2007 Antoine Ginies <aginies@mandriva.com> 1.4.0-1mdv2008.0
+ Revision: 29139
- release 1.4.0


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

* Tue Sep 02 2003 Abel Cheung <deaddog@deaddog.org> 1.0.6-4mdk
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

