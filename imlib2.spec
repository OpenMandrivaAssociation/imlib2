%define major	1
%define libname	%mklibname %{name}_ %{major}
%define develname %mklibname %name -d

Name:		imlib2
Version:	1.4.4
Release:	3
Summary:	Powerful image loading and rendering library
License:	Imlib2
URL:		http://enlightenment.org/Libraries/Imlib2/
Group:		System/Libraries
# Same as upstream tarball except the copyright-breaking /data/fonts
# subdirectory is entirely removed - AdamW 2008/03
Source0:	http://sourceforge.net/projects/enlightenment/files/imlib2-src/%version/%name-%version.tar.bz2
# Drop data/fonts from the build, it only contains copyright-
# infringing fonts - AdamW 2008/03 (#38258)
Patch4:		imlib2-1.4.2-fontclean.patch
BuildRequires:	freetype2-devel
BuildRequires:	jpeg-devel
BuildRequires:	png-devel
BuildRequires:	libtiff-devel
BuildRequires:	ungif-devel
BuildRequires:	libx11-devel libxext-devel
BuildRequires:	id3tag-devel

%description
Imlib2 is an advanced replacement library for libraries like libXpm that
provides many more features with much greater flexibility and speed than
standard libraries, including font rasterization, rotation, RGBA space
rendering and blending, dynamic binary filters, scripting, and more.

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


%package -n	%{develname}
Summary:	Imlib2 headers, static libraries and documentation
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
# (tv) only ever released major was 1, so keep smooth upgrading for old distro in future releases:
Obsoletes:	%mklibname %{name}_ 1 -d

%description -n	%{develname}
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

%description -n	%{libname}-filters
This package contains Imlib2 basic set of plugin filters.

%package -n	%{libname}-loaders
Summary:	Imlib2 loader for various graphic formats
Group:		System/Libraries

%description -n	%{libname}-loaders
This package contains Imlib2 image loader/saver for various graphic formats,
such as jpeg, gif, tiff, xpm etc.

%package	data
Summary:	Imlib2 data
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}
BuildArch:	noarch

%description	data
This package contains Imlib2 data.

%prep
%setup -q
%patch4 -p1 -b .font~

%build
autoreconf -fi
%configure2_5x
%make

%install
%makeinstall_std

# remove files not bundled
rm -f	%{buildroot}%{_libdir}/%{name}/loaders/*.a \
	%{buildroot}%{_libdir}/%{name}/filters/*.a

%multiarch_binaries %{buildroot}%{_bindir}/imlib2-config

%files -n %{libname}
%doc AUTHORS README COPYING
%{_libdir}/lib*.so.*

%files -n %{develname}
%doc ChangeLog doc/index.html doc/imlib2.gif doc/blank.gif
%{_bindir}/*
%{_bindir}/imlib2-config
%{_libdir}/lib*.so
%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*

%files -n %{libname}-filters
%{_libdir}/%{name}/filters

%files -n %{libname}-loaders
%{_libdir}/%{name}/loaders

%files data
%{_datadir}/%{name}
