Summary:	Common Language Infrastructure implementation
Summary(pl):	Implementacja jêzyka CLI
Name:		mono
Version:	0.7
Release:	2
License:	GPL
Group:		Development/Languages
Source0:	http://www.go-mono.com/archive/%{name}-%{version}.tar.gz
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-ac_fixes.patch
URL:		http://www.go-mono.com/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	glib-devel >= 1.2.0
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Common Language Infrastructure platform. Microsoft has created a
new development platform. The highlights of this new development
platform are:
- A runtime environment that provides garbage collection, threading
  and a virtual machine specification (The Virtual Execution System,
  VES),
- A comprehensive class library,
- A new language, C#. Very similar to Java, C# allows programmers to
  use all the features available on the .NET runtime,
- A language specification that compilers can follow if they want to
  generate classes and code that can interoperate with other programming
  languages (The Common Language Specification: CLS).

%description -l pl
Platforma CLI (Common Language Infrastructure). Microsoft stworzy³
now± platformê developersk±. Zalety tej platformy to:
- ¶rodowisko, które dostarsza garbale collector, w±tki oraz
  specyfikacjê maszyny wirtualnej (The Virtual Execution System, VES),
- bibliotekê klas,
- nowy jêzyk, C#. Bardzo podobny do Javy, C# pozwala programistom na
  u¿ywanie wszystkich mo¿liwo¶ci dostarczanych przez platformê .NET,
- specyfikacja dla kompilatorów, które chc± generowaæ kod
  wspó³pracuj±cy z innymi jêzykami programowania (The Common Language
  Specification: CLS).

%package devel
Summary:	Development resources for mono
Summary(pl):	Zasoby programisty do mono
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Development resources for mono.

%description devel -l pl
Zasoby programosty do mono.

%package static
Summary:	Static mono library
Summary(pl):	Statyczna biblioteka mono
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static mono library.

%description static -l pl
Statyczna biblioteka mono.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
rm -f missing
%{__libtoolize}
aclocal
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	assembliesdir=%{_libdir}

rm -f doc/Makefile*

gzip -9nf AUTHORS ChangeLog NEWS README doc/*

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/*.so.*.*
%attr(755,root,root) %{_libdir}/*.dll
%{_datadir}/%{name}
%{_mandir}/man?/*

%files devel
%defattr(644,root,root,755)
%doc *.gz doc
%attr(755,root,root) %{_libdir}/*.la
%attr(755,root,root) %{_libdir}/*.so
%{_includedir}/%{name}

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
