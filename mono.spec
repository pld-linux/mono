Summary:	Common Language Infrastructure implementation
Summary(pl):	Implementacja jêzyka CLI
Name:		mono
Version:	0.7
Release:	1
License:	GPL
Group:		Development/Languages
Group(de):	Entwicklung/Sprachen
Group(pl):	Programowanie/Jêzyki
Source0:	http://www.go-mono.com/archive/%{name}-%{version}.tar.gz
URL:		http://www.go-mono.com/
BuildRequires:	glib-devel >= 1.2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Common Language Infrastructure platform. Microsoft has created a
new development platform. The highlights of this new development
platform are:
- A runtime environment that provides garbage collection, threading
  and a virtual machine specification (The Virtual Execution System,
  VES)
- A comprehensive class library.
- A new language, C#. Very similar to Java, C# allows programmers to
  use all the features available on the .NET runtime.
- A language specification that compilers can follow if they want to
  generate classes and code that can interoperate with other programming
  languages (The Common Language Specification: CLS)

%description -l pl
Platforma CLI (Common Language Infrastructure). Microsoft stworzy³
now± platformê developersk±. Zalety tej platformy to:
- ¶rodowisko, które dostarsza garbale collector, w±tki oraz
  specyfikacjê maszyny wirtualnej (The Virtual Execution System, VES)
- bibliotekê klas
- nowy jêzyk, C#. Bardzo podobny do Javy, C# pozwala programistom na
  u¿ywanie wszystkich mo¿liwo¶ci dostarczanych przez platformê .NET
- specyfikacja dla kompilatorów, które chc± generowaæ kod
  wspó³pracuj±cy z innymi jêzykami programowania (The Common Language
  Specification: CLS)
%prep
%setup -q

%build
%configure2_13
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	assembliesdir=$RPM_BUILD_ROOT%{_libdir} \
	DESTDIR=$RPM_BUILD_ROOT

rm -f doc/Makefile*

gzip -9nf AUTHORS ChangeLog NEWS README doc/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz doc
%attr(755,root,root) %{_bindir}/*
%{_includedir}/%{name}
%attr(755,root,root) %{_libdir}/*.dll
%attr(755,root,root) %{_libdir}/*.so*
%attr(755,root,root) %{_libdir}/*.la
%{_libdir}/*.a
%{_datadir}/%{name}
%{_mandir}/man?/*
