Summary:	Common Language Infrastructure implementation
Summary(pl):	Implementacja j�zyka CLI
Name:		mono
Version:	0.21
Release:	2
License:	LGPL
Group:		Development/Languages
Source0:	http://www.go-mono.com/archive/%{name}-%{version}.tar.gz
Source1:	http://www.go-mono.com/archive/mcs-%{version}.tar.gz
URL:		http://www.go-mono.com/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gc-devel >= 6.0-3
BuildRequires:	glib2-devel
BuildRequires:	libtool
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
Platforma CLI (Common Language Infrastructure). Microsoft stworzy�
now� platform� developersk�. Zalety tej platformy to:
- �rodowisko, kt�re dostarsza garbale collector, w�tki oraz
  specyfikacj� maszyny wirtualnej (The Virtual Execution System, VES),
- bibliotek� klas,
- nowy j�zyk, C#. Bardzo podobny do Javy, C# pozwala programistom na
  u�ywanie wszystkich mo�liwo�ci dostarczanych przez platform� .NET,
- specyfikacja dla kompilator�w, kt�re chc� generowa� kod
  wsp�pracuj�cy z innymi j�zykami programowania (The Common Language
  Specification: CLS).

%package devel
Summary:	Development resources for mono
Summary(pl):	Zasoby programisty do mono
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Development resources for mono.

%description devel -l pl
Zasoby programisty dla mono.

%package basic
Summary:	MonoBASIC compiler for mono
Summary(pl):	Kompilator MonoBASIC dla mono
Group:		Development/Languages
Requires:	%{name}-devel = %{version}

%description basic
MonoBASIC compiler for mono.

%description basic -l pl
Kompilator MonoBASIC dla mono.

%package csharp
Summary:	C# compiler for mono
Summary(pl):	Kompilator C# dla mono
Group:		Development/Languages
Requires:	%{name}-devel = %{version}

%description csharp
C# compiler for mono.

%description csharp -l pl
Kompilator C# dla mono.

%package ilasm
Summary:	ILasm compiler for mono
Summary(pl):	Kompilator ILasm dla mono
Group:		Development/Languages
Requires:	%{name}-devel = %{version}

%description ilasm
ILasm compiler for mono.

%description ilasm -l pl
Kompilator ILasm dla mono.

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
%setup -q -a1

%build
rm -f missing
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure --with-gc=boehm
%{__make}

# for now we only build jay, and don't rebuild runtime and mcs
%{__make} -C mcs-%{version}/jay CC=%{__cc} CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
	
install mcs-%{version}/jay/jay $RPM_BUILD_ROOT%{_bindir}/
install mcs-%{version}/jay/jay.1 $RPM_BUILD_ROOT%{_mandir}/man1

%ifnarch %{ix86}
ln -s mint $RPM_BUILD_ROOT%{_bindir}/mono
%endif

# Make links to all binaries. In fact we could move *.exe to 
# %{_libdir}, but probably something relays on it.
old="$(pwd)"
cd $RPM_BUILD_ROOT%{_bindir}
for f in *.exe ; do
	bn=$(basename $f .exe)
	rm -f $bn
	echo "#!/bin/sh" > $bn
	echo "%{_bindir}/mono %{_bindir}/$f" '"$@"' >> $bn
done
cd "$old"


# this way we can run rpmbuild -bi several times, and directories
# have more meaningful name.
rm -rf pld-doc
mkdir -p pld-doc/{webpage,notes}
cp -a doc/* pld-doc/webpage/
cp -a docs/* pld-doc/notes/
rm -f pld-doc/*/Makefile*

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mint
%attr(755,root,root) %{_bindir}/mono
%attr(755,root,root) %{_bindir}/secutil*
%attr(755,root,root) %{_bindir}/monosn
%ifarch %{ix86}
%attr(755,root,root) %{_libdir}/*.so.*.*
%endif
%attr(755,root,root) %{_libdir}/*.dll
%{_mandir}/man5/mono-config.5*
%{_mandir}/man1/mint.1*
%{_mandir}/man1/mono.1*
%dir %{_sysconfdir}/mono
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mono/config
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mono/machine.config

%files devel
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README pld-doc/*
%attr(755,root,root) %{_bindir}/monodis
%attr(755,root,root) %{_bindir}/monograph
%attr(755,root,root) %{_bindir}/monoresgen*
%attr(755,root,root) %{_bindir}/pedump
%attr(755,root,root) %{_bindir}/sqlsharp*
%attr(755,root,root) %{_bindir}/jay
%ifarch %{ix86}
%{_libdir}/*.la
%attr(755,root,root) %{_libdir}/*.so
%endif
%{_datadir}/%{name}
%{_libdir}/pkgconfig/*
%{_includedir}/%{name}
%{_mandir}/man1/jay.1*
%{_mandir}/man1/monoburg.1*
%{_mandir}/man1/monodis.1*
%{_mandir}/man1/monostyle.1*
%{_mandir}/man1/sqlsharp.1*

%files csharp
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mcs*
%{_mandir}/man1/mcs.1*

%files basic
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mbas*

%files ilasm
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ilasm*

%files static
%defattr(644,root,root,755)
%ifarch %{ix86}
%{_libdir}/lib*.a
%endif
