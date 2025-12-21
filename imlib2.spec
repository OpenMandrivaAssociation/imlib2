%define major 1
%define libname %mklibname %{name}
%define boguslibname %mklibname %{name}_
%define oldlibname %mklibname %{name}_ 1
%define devname %mklibname %{name} -d

Summary:	Powerful image loading and rendering library
Name:		imlib2
Version:	1.12.5
Release:	2
License:	Imlib2
Group:		System/Libraries
Url:		https://enlightenment.org/Libraries/Imlib2/
Source0:	https://sourceforge.net/projects/enlightenment/files/imlib2-src/%{version}/%{name}-%{version}.tar.xz

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool-base
BuildRequires:	slibtool
BuildRequires:	make
BuildRequires:	pkgconfig(bzip2)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libtiff-4)
# libheif lives in restriced due to licensing
#BuildRequires:	pkgconfig(libheif)
BuildRequires:	pkgconfig(libopenjp2)
# libwebp causes linker errors
#BuildRequires:	pkgconfig(libwebp)
#BuildRequires:	pkgconfig(libwebpdemux)
BuildRequires:	ungif-devel
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(id3tag)
BuildRequires:	pkgconfig(libpng)
BuildRequires:  pkgconfig(xcb)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libjxl)
BuildRequires:  pkgconfig(libjxl_threads)
BuildRequires:  pkgconfig(librsvg-2.0) >= 2.46
BuildRequires:  pkgconfig(libspectre)


%description
Imlib2 is an advanced replacement library for libraries like libXpm that
provides many more features with much greater flexibility and speed than
standard libraries, including font rasterization, rotation, RGBA space
rendering and blending, dynamic binary filters, scripting, and more.

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Powerful image loading and rendering library
Group:		System/Libraries
# Fixed after 5.0
%rename %{oldlibname}
# Fixed after 5.0
%rename %{boguslibname}
Provides:	%{name} = %{EVRD}
Requires:	%{libname}-filters = %{EVRD}
Requires:	%{libname}-loaders = %{EVRD}

%description -n %{libname}
Imlib2 is an advanced replacement library for libraries like libXpm that
provides many more features with much greater flexibility and speed than
standard libraries, including font rasterization, rotation, RGBA space
rendering and blending, dynamic binary filters, scripting, and more.

%files -n %{libname}
%doc AUTHORS README COPYING
%{_libdir}/libImlib2.so.%{major}*
%{_datadir}/imlib2

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Imlib2 headers, development libraries and documentation
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
# taken from fedora where the demos and data are simply removed
Obsoletes:	%{name}-data < 1.4.5-3

%description -n %{devname}
Imlib2 is an advanced replacement library for libraries like libXpm that
provides many more features with much greater flexibility and speed than
standard libraries, including font rasterization, rotation, RGBA space
rendering and blending, dynamic binary filters, scripting, and more.

This package contains various headers and development libraries for %{name}.
You need this package if you want to compile or develop any applications
that need %{name}.

%files -n %{devname}
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*

#----------------------------------------------------------------------------

%package -n %{libname}-filters
Summary:	Imlib2 basic plugin filters set
Group:		System/Libraries
Obsoletes:	lib64imlib2_1-filters

%description -n %{libname}-filters
This package contains Imlib2 basic set of plugin filters.

%files -n %{libname}-filters
%{_libdir}/%{name}/filters

#----------------------------------------------------------------------------

%package -n %{libname}-loaders
Summary:	Imlib2 loader for various graphic formats
Group:		System/Libraries
Obsoletes:	lib64imlib2_1-loaders
Provides:	%{name}-loaders = %{version}-%{release}

%description -n %{libname}-loaders
This package contains Imlib2 image loader/saver for various graphic formats,
such as jpeg, gif, tiff, xpm etc.

%files -n %{libname}-loaders
%{_libdir}/%{name}/loaders

#----------------------------------------------------------------------------

%prep
%autosetup -p1
#sed -i 's/@my_libs@//' imlib2-config.in

autoreconf -fi

%build
%configure \
	--disable-static \
	--enable-shared \
	--with-jxl \
	--with-svg \
	--with-ps \
%ifarch x86_64
	--enable-amd64 \
	--disable-mmx \
%endif
%ifarch ix86
	--disable-amd64 \
	--enable-mmx \
%endif
	--enable-visibility-hiding
%make_build

%install
%make_install

# remove demos and their dependencies
rm -f %{buildroot}%{_bindir}/imlib2_*
rm -rf %{buildroot}%{_datadir}/imlib2/data/
