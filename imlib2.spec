%define major	1
%define libname	%mklibname %{name}_ %{major}
%define devname %mklibname %{name} -d

Summary:	Powerful image loading and rendering library
Name:		imlib2
Version:	1.4.5
Release:	8
License:	Imlib2
Group:		System/Libraries
Url:		http://enlightenment.org/Libraries/Imlib2/
# Same as upstream tarball except the copyright-breaking /data/fonts
# subdirectory is entirely removed - AdamW 2008/03
Source0:	http://sourceforge.net/projects/enlightenment/files/imlib2-src/%{version}/%{name}-%{version}.tar.bz2
Patch0:		imlib2-automake-1.13.patch
# Drop data/fonts from the build, it only contains copyright-
# infringing fonts - AdamW 2008/03 (#38258)
Patch4:		imlib2-1.4.2-fontclean.patch
Patch5:		imlib2-1.4.5-giflib5.patch

BuildRequires:	bzip2-devel
BuildRequires:	jpeg-devel
BuildRequires:	tiff-devel
BuildRequires:	ungif-devel
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(id3tag)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)

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

%package -n %{devname}
Summary:	Imlib2 headers, development libraries and documentation
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
# taken from fedora where the demos and data are simply removed
Obsoletes:	%{name}-data < 1.4.5-3

%description -n	%{devname}
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
%apply_patches
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
%{_libdir}/libImlib2.so.%{major}*

%files -n %{devname}
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

