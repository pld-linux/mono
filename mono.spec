Summary:	Common Language Infrastructure implementation
Summary(pl):	Implementacja jêzyka CLI
Name:		mono
Version:	0.13
Release:	1
License:	LGPL
Group:		Development/Languages
Source0:	http://www.go-mono.com/archive/%{name}-%{version}.tar.gz
URL:		http://www.go-mono.com/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	glib2-devel
BuildRequires:	libtool
BuildRequires:	gc-devel >= 6.0-3
BuildRequires:	pkgconfig
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

%build
rm -f missing
%{__libtoolize}
aclocal
%{__autoconf}
%{__automake}
%configure --with-gc=boehm
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT 

rm -f doc/Makefile* docs/Makefile*

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mint
%attr(755,root,root) %{_bindir}/mono
%attr(755,root,root) %{_libdir}/*.so.*.*
%attr(755,root,root) %{_libdir}/*.dll
%{_mandir}/man5/mono-config.5*
%{_mandir}/man1/mint.1*
%{_mandir}/man1/mono.1*

%files devel
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README doc docs
%attr(755,root,root) %{_bindir}/mcs*
%attr(755,root,root) %{_bindir}/monodis
%attr(755,root,root) %{_bindir}/monograph
%attr(755,root,root) %{_libdir}/*.la
%attr(755,root,root) %{_libdir}/*.so
%{_datadir}/%{name}
%{_libdir}/pkgconfig/*
%{_includedir}/%{name}
%{_mandir}/man1/mcs.1*
%{_mandir}/man1/monoburg.1*
%{_mandir}/man1/monodis.1*
%{_mandir}/man1/monostyle.1*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
