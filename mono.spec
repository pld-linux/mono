Summary:	Common Language Infrastructure implementation
Summary(pl):	Implementacja Common Language Infrastructure
Name:		mono
Version:	0.26
Release:	3
License:	LGPL
Group:		Development/Languages
Source0:	http://www.go-mono.com/archive/%{name}-%{version}.tar.gz
# Source0-md5:	6821b1e8e4493109d9d42a90a631223a
Source1:	http://www.go-mono.com/archive/mcs-%{version}.tar.gz
# Source1-md5:	4ccc74667ff4d79ba08b341d2e684921
Patch0:		%{name}-nolibs.patch
URL:		http://www.go-mono.com/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
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
Platforma CLI (Common Language Infrastructure). Microsoft stworzy³
now± platformê developersk±. Zalety tej platformy to:
- ¶rodowisko, które dostarsza garbage collector, w±tki oraz
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
Provides:	ilasm
Obsoletes:	pnet-compiler-ilasm

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

%package jay
Summary:	Yacc-like parser generator for Java and C#
Summary(pl):	Podobny do Yacca generator parserów dla Javy i C#
Group:		Development/Tools

%description jay
Yacc-like parser generator for Java and C#.

%description jay -l pl
Podobny do Yacca generator parserów dla Javy i C#.

%prep
%setup -q -a1
%patch -p1

%build
rm -f missing
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--with-gc=boehm

%{__make}

# for now we only build jay, and don't rebuild runtime and mcs
%{__make} -C mcs-%{version}/jay \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -DSKEL_DIRECTORY=\\\"%{_datadir}/jay\\\""

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C mcs-%{version}/jay install \
	prefix=%{_prefix} \
	DESTDIR=$RPM_BUILD_ROOT
mv -f $RPM_BUILD_ROOT%{_prefix}/man/man1/* $RPM_BUILD_ROOT%{_mandir}/man1
rm -f $RPM_BUILD_ROOT%{_datadir}/jay/[A-Z]*

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
#%attr(755,root,root) %{_bindir}/oldmono
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%endif
%attr(755,root,root) %{_libdir}/*.dll
%{_mandir}/man5/mono-config.5*
%{_mandir}/man1/mint.1*
%{_mandir}/man1/mono.1*
#%{_mandir}/man1/oldmono.1*
%dir %{_sysconfdir}/mono
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mono/config
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mono/machine.config

%files jay
%defattr(644,root,root,755)
%doc mcs-%{version}/jay/{ACKNOWLEDGEMENTS,ChangeLog,NEW_FEATURES,NOTES,README,README.jay}
%attr(755,root,root) %{_bindir}/jay
%dir %{_datadir}/jay
%{_datadir}/jay/skeleton*
%{_mandir}/man1/jay.1*

%files devel
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README pld-doc/*
%attr(755,root,root) %{_bindir}/monodis
%attr(755,root,root) %{_bindir}/xsd*
%attr(755,root,root) %{_bindir}/monograph
%attr(755,root,root) %{_bindir}/monoresgen*
%attr(755,root,root) %{_bindir}/pedump
%attr(755,root,root) %{_bindir}/sqlsharp*
#%ifarch %{ix86}
#%attr(755,root,root) %{_bindir}/genmdesc
#%endif
%attr(755,root,root) %{_bindir}/cilc*
%ifarch %{ix86}
%{_libdir}/lib*.la
%attr(755,root,root) %{_libdir}/lib*.so
%endif
%{_datadir}/%{name}
%{_pkgconfigdir}/*.pc
%{_includedir}/%{name}
%{_mandir}/man1/cilc.1*
%{_mandir}/man1/monoburg.1*
%{_mandir}/man1/monodis.1*
%{_mandir}/man1/monostyle.1*
%{_mandir}/man1/sqlsharp.1*
%{_mandir}/man1/cert2spc.1*

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
%{_mandir}/man1/ilasm.1*

%ifarch %{ix86}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%endif
