%define	name	imlib2
%define	version 1.4.0
%define release	%mkrel 1
%define major	1
%define libname	%mklibname %{name}_ %{major}
%define enable_mmx 0
%{?_with_mmx: %global enable_mmx 1}

Name:		%{name}
Version: 1.4.0.000
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

